# LangChain Dependencies - Add these to requirements.txt
"""
langchain==0.1.0
langchain-openai==0.0.5
langchain-community==0.0.10
faiss-cpu==1.7.4
"""

import os
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class CareerAgentLangChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize memory for conversation context
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=5  # Keep last 5 exchanges
        )
        
        # Create tools for the agent
        self.tools = self._create_tools()
        
        # Create the agent
        self.agent = self._create_agent()
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _create_tools(self) -> List[Tool]:
        """Create tools that the agent can use"""
        
        def job_market_research(query: str) -> str:
            """Research current job market trends for a specific role or industry"""
            # This could integrate with job APIs, but for now we'll simulate
            prompt = f"""
            As a job market analyst, provide current market insights for: {query}
            Include:
            1. Job demand and growth prospects
            2. Average salary ranges
            3. Required skills and qualifications
            4. Top hiring companies
            5. Geographic hotspots
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def skill_gap_analysis(current_skills: str, target_role: str) -> str:
            """Analyze skill gaps between current abilities and target role requirements"""
            prompt = f"""
            Current Skills: {current_skills}
            Target Role: {target_role}
            
            Provide a detailed skill gap analysis including:
            1. Skills you already have that match
            2. Missing technical skills
            3. Soft skills to develop
            4. Learning priority order
            5. Estimated time to acquire each skill
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def career_path_planner(current_position: str, career_goals: str) -> str:
            """Create a structured career progression plan"""
            prompt = f"""
            Current Position: {current_position}
            Career Goals: {career_goals}
            
            Create a 5-year career roadmap including:
            1. Year-by-year progression steps
            2. Key milestones and achievements
            3. Skills to develop each year
            4. Networking and experience goals
            5. Potential challenges and mitigation strategies
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def interview_preparation(role: str, company_type: str = "general") -> str:
            """Generate targeted interview preparation materials"""
            prompt = f"""
            Role: {role}
            Company Type: {company_type}
            
            Provide comprehensive interview prep including:
            1. 10 common technical questions
            2. 5 behavioral questions with STAR method examples
            3. Questions to ask the interviewer
            4. Company research tips
            5. Salary negotiation strategies
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="job_market_research",
                description="Research current job market trends, salary ranges, and demand for specific roles",
                func=job_market_research
            ),
            Tool(
                name="skill_gap_analysis",
                description="Analyze the gap between current skills and target role requirements",
                func=skill_gap_analysis
            ),
            Tool(
                name="career_path_planner",
                description="Create structured career progression plans and roadmaps",
                func=career_path_planner
            ),
            Tool(
                name="interview_preparation",
                description="Generate comprehensive interview preparation materials for specific roles",
                func=interview_preparation
            )
        ]
    
    def _create_agent(self):
        """Create the LangChain agent with custom prompt"""
        
        system_prompt = """
        You are an expert AI Career Coach with access to specialized tools for career guidance.
        
        Your capabilities include:
        - Job market research and trend analysis
        - Skill gap identification and learning recommendations
        - Career path planning and progression strategies
        - Interview preparation and coaching
        - Resume optimization advice
        - Networking and professional development guidance
        
        Guidelines:
        1. Always use relevant tools to provide data-driven advice
        2. Personalize recommendations based on user's background
        3. Provide actionable, specific guidance
        4. Consider current market conditions and trends
        5. Be encouraging while being realistic about challenges
        
        When a user asks for career advice, think about which tools would be most helpful
        and use them to provide comprehensive, well-researched guidance.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def get_career_advice(self, query: str, user_context: Dict[str, Any] = None) -> str:
        """
        Get comprehensive career advice using LangChain agent
        
        Args:
            query: User's career question or goal
            user_context: Optional context like current role, skills, experience level
        """
        
        # Enhance query with context if provided
        if user_context:
            context_str = ", ".join([f"{k}: {v}" for k, v in user_context.items()])
            enhanced_query = f"Context: {context_str}\n\nQuestion: {query}"
        else:
            enhanced_query = query
        
        try:
            response = self.agent_executor.invoke({
                "input": enhanced_query
            })
            return response["output"]
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"


class InterviewAgentLangChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.8,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10
        )
        
        self.tools = self._create_interview_tools()
        self.agent = self._create_interview_agent()
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    
    def _create_interview_tools(self) -> List[Tool]:
        """Create interview-specific tools"""
        
        def generate_technical_questions(role: str, difficulty: str = "medium") -> str:
            """Generate role-specific technical interview questions"""
            prompt = f"""
            Generate 10 technical interview questions for: {role}
            Difficulty level: {difficulty}
            
            Include:
            1. Programming/technical skill questions
            2. System design questions (if applicable)
            3. Problem-solving scenarios
            4. Code review questions
            5. Architecture and best practices
            
            Format each question with expected answer guidelines.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def behavioral_questions_generator(role: str, company_culture: str = "collaborative") -> str:
            """Generate behavioral interview questions with STAR method examples"""
            prompt = f"""
            Generate 8 behavioral interview questions for: {role}
            Company culture: {company_culture}
            
            For each question, provide:
            1. The question
            2. What the interviewer is looking for
            3. A sample STAR method answer
            4. Common mistakes to avoid
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def mock_interview_simulator(role: str, question_type: str = "mixed") -> str:
            """Simulate a realistic interview scenario"""
            prompt = f"""
            Conduct a mock interview for: {role}
            Question type: {question_type}
            
            Provide:
            1. 5 progressive interview questions (easy to hard)
            2. Follow-up questions based on typical answers
            3. Evaluation criteria for each question
            4. Feedback on how to improve answers
            5. Overall interview performance assessment framework
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="generate_technical_questions",
                description="Generate role-specific technical interview questions with answer guidelines",
                func=generate_technical_questions
            ),
            Tool(
                name="behavioral_questions_generator", 
                description="Create behavioral interview questions with STAR method examples",
                func=behavioral_questions_generator
            ),
            Tool(
                name="mock_interview_simulator",
                description="Simulate realistic interview scenarios with progressive difficulty",
                func=mock_interview_simulator
            )
        ]
    
    def _create_interview_agent(self):
        """Create interview coaching agent"""
        
        system_prompt = """
        You are an expert Interview Coach with specialized tools for interview preparation.
        
        Your role is to:
        1. Generate realistic, role-specific interview questions
        2. Provide behavioral interview coaching using STAR method
        3. Conduct mock interview simulations
        4. Give detailed feedback on interview performance
        5. Help candidates prepare for technical and cultural fit assessments
        
        Always use your tools to provide comprehensive, realistic interview preparation
        that matches current industry standards and best practices.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def get_interview_questions(self, role: str, question_type: str = "comprehensive") -> str:
        """Generate comprehensive interview questions for a specific role"""
        
        query = f"""
        I'm preparing for a {role} interview. Please help me prepare by:
        1. Generating relevant technical questions
        2. Creating behavioral questions appropriate for this role
        3. Setting up a mock interview scenario
        
        Question focus: {question_type}
        """
        
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"


# Usage examples and integration with Flask
def integrate_langchain_with_flask():
    """Example of how to integrate with your Flask app"""
    
    # Initialize agents globally or use singleton pattern
    career_agent = CareerAgentLangChain()
    interview_agent = InterviewAgentLangChain()
    
    def get_career_advice_langchain(query: str, user_context: Dict = None) -> str:
        """Enhanced career advice function using LangChain"""
        return career_agent.get_career_advice(query, user_context)
    
    def get_interview_questions_langchain(role: str) -> str:
        """Enhanced interview questions using LangChain"""
        return interview_agent.get_interview_questions(role)
    
    return get_career_advice_langchain, get_interview_questions_langchain


# Example of advanced features you can add:

class AdvancedCareerFeatures:
    """Additional advanced features using LangChain"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        
    def career_document_analysis(self, resume_text: str, job_description: str) -> str:
        """Analyze resume against specific job descriptions"""
        
        # Create embeddings for semantic similarity
        embeddings = OpenAIEmbeddings()
        
        # Split documents for analysis
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        resume_chunks = text_splitter.split_text(resume_text)
        job_chunks = text_splitter.split_text(job_description)
        
        # Create vector stores for semantic search
        resume_vectorstore = FAISS.from_texts(resume_chunks, embeddings)
        job_vectorstore = FAISS.from_texts(job_chunks, embeddings)
        
        # Perform similarity analysis
        # This is a simplified example - you'd want more sophisticated analysis
        
        prompt = f"""
        Analyze this resume against the job description:
        
        Resume: {resume_text[:1000]}...
        Job Description: {job_description[:1000]}...
        
        Provide:
        1. Match percentage and reasoning
        2. Strengths that align well
        3. Missing qualifications
        4. Suggestions for resume improvements
        5. Keywords to add
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content
