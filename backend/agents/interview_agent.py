
"""
Enhanced Interview Agent using LangChain Framework
Comprehensive interview preparation with specialized coaching tools
"""

import os
from typing import List, Dict, Any, Optional
try:
    from langchain_openai import ChatOpenAI
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain.tools import Tool
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.schema import HumanMessage
    from langchain.memory import ConversationBufferWindowMemory
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    from utils.openai_helper import agentic_completion

class InterviewAgentLangChain:
    """Enhanced Interview Agent using LangChain framework"""
    
    def __init__(self):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not installed. Install with: pip install langchain langchain-openai")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=5
        )
        
        self.tools = self._create_interview_tools()
        self.agent_executor = self._create_agent()
    
    def _create_interview_tools(self) -> List[Tool]:
        """Create interview-specific tools for comprehensive preparation"""
        
        def question_generator(role_level_company: str) -> str:
            """Generate targeted interview questions by category and difficulty"""
            prompt = f"""
            Role/Level/Company Context: {role_level_company}
            
            Generate comprehensive interview question bank:
            
            1. BEHAVIORAL QUESTIONS (STAR Method):
               - Leadership and team management scenarios
               - Problem-solving and critical thinking challenges
               - Conflict resolution and difficult situations
               - Achievement and success stories
               - Failure and learning experiences
               - Adaptability and change management
               - Communication and collaboration examples
            
            2. TECHNICAL QUESTIONS (Role-Specific):
               - Core technical competency assessment
               - System design and architecture challenges
               - Problem-solving coding exercises
               - Best practices and methodology knowledge
               - Troubleshooting and debugging scenarios
               - Performance optimization questions
               - Security and scalability considerations
            
            3. SITUATIONAL JUDGMENT QUESTIONS:
               - Ethical dilemma scenarios
               - Priority and resource management
               - Stakeholder management challenges
               - Innovation and creativity prompts
               - Customer service situations
               - Quality vs deadline tradeoffs
               - Team dynamics and culture fit
            
            4. COMPANY AND ROLE-SPECIFIC QUESTIONS:
               - Industry knowledge and trends
               - Company culture and values alignment
               - Role-specific responsibilities understanding
               - Growth and development aspirations
               - Contribution and value proposition
               - Long-term career vision alignment
            
            5. REVERSE INTERVIEW QUESTIONS:
               - Strategic questions to ask the interviewer
               - Company culture and team dynamics
               - Growth opportunities and career path
               - Technical challenges and innovation
               - Performance expectations and success metrics
            
            Provide 20-25 high-quality questions across all categories with difficulty levels.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def answer_coach(question_answer_context: str) -> str:
            """Provide coaching for interview answer improvement"""
            prompt = f"""
            Question/Answer/Context: {question_answer_context}
            
            Provide comprehensive answer coaching:
            
            1. ANSWER STRUCTURE ANALYSIS:
               - STAR method application (Situation, Task, Action, Result)
               - Logical flow and organization
               - Introduction, body, and conclusion balance
               - Time management and conciseness
               - Key message clarity and impact
            
            2. CONTENT IMPROVEMENT:
               - Specific examples and quantifiable results
               - Technical depth and accuracy
               - Business value and impact demonstration
               - Leadership and initiative showcase
               - Problem-solving approach clarity
            
            3. DELIVERY ENHANCEMENT:
               - Confidence and enthusiasm projection
               - Body language and eye contact tips
               - Voice modulation and pacing
               - Nervousness management techniques
               - Active listening and engagement
            
            4. COMMON PITFALLS TO AVOID:
               - Rambling and off-topic responses
               - Negative language about previous roles
               - Lack of specific examples
               - Overselling or underselling abilities
               - Poor preparation indicators
            
            5. STRENGTH AMPLIFICATION:
               - Unique value proposition emphasis
               - Competitive advantage highlighting
               - Cultural fit demonstration
               - Growth mindset and learning agility
               - Passion and motivation communication
            
            6. FOLLOW-UP STRATEGIES:
               - Clarifying questions when needed
               - Building on interviewer responses
               - Connecting answers to role requirements
               - Transitioning between topics smoothly
               - Thank you and next steps communication
            
            Provide specific, actionable feedback with improved answer examples.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def company_research_analyst(company_role_info: str) -> str:
            """Analyze company and role for strategic interview preparation"""
            prompt = f"""
            Company/Role Information: {company_role_info}
            
            Conduct comprehensive company and role analysis:
            
            1. COMPANY INTELLIGENCE:
               - Business model and revenue streams
               - Market position and competitive landscape
               - Recent news, funding, and strategic initiatives
               - Company culture and core values
               - Leadership team and organizational structure
               - Growth trajectory and future outlook
               - Industry trends and challenges
            
            2. ROLE ANALYSIS:
               - Position responsibilities and expectations
               - Required vs preferred qualifications
               - Team structure and reporting relationships
               - Key performance indicators and success metrics
               - Growth opportunities and career progression
               - Budget and resource management scope
               - Cross-functional collaboration requirements
            
            3. INTERVIEWER PREPARATION:
               - Potential interviewer backgrounds and roles
               - Interview process and typical format
               - Assessment criteria and evaluation methods
               - Common questions and challenge areas
               - Company-specific interview culture
               - Decision-making timeline and process
            
            4. STRATEGIC POSITIONING:
               - Value proposition alignment with company needs
               - Unique differentiators and competitive advantages
               - Relevant experience and skill highlighting
               - Cultural fit demonstration strategies
               - Passion and motivation communication
               - Long-term commitment and growth vision
            
            5. INTELLIGENT QUESTIONS TO ASK:
               - Strategic business questions
               - Team dynamics and collaboration
               - Technology stack and innovation
               - Professional development opportunities
               - Performance expectations and feedback
               - Company vision and future direction
            
            6. RED FLAGS AND CONSIDERATIONS:
               - Potential concerns or challenges
               - Cultural misalignment indicators
               - Growth limitation factors
               - Work-life balance considerations
               - Compensation and benefits evaluation
               - Alternative opportunity comparison
            
            Provide strategic insights and actionable preparation recommendations.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def mock_interview_simulator(interview_parameters: str) -> str:
            """Simulate realistic interview scenarios with feedback"""
            prompt = f"""
            Interview Parameters: {interview_parameters}
            
            Conduct comprehensive mock interview simulation:
            
            1. INTERVIEW SETUP:
               - Realistic interview format and structure
               - Time allocation for different segments
               - Interviewer persona and background
               - Assessment criteria and focus areas
               - Technology setup for virtual interviews
            
            2. QUESTION PROGRESSION:
               - Warm-up and rapport building questions
               - Core competency assessment questions
               - Technical challenge or case study
               - Behavioral and situational scenarios
               - Company and role-specific inquiries
               - Candidate questions and engagement
            
            3. PERFORMANCE EVALUATION:
               - Answer quality and completeness
               - Technical accuracy and depth
               - Communication clarity and confidence
               - Problem-solving approach and methodology
               - Cultural fit and enthusiasm demonstration
               - Professional presence and engagement
            
            4. REAL-TIME FEEDBACK:
               - Immediate improvement suggestions
               - Body language and delivery notes
               - Content enhancement opportunities
               - Time management observations
               - Nervousness and confidence indicators
            
            5. POST-INTERVIEW ANALYSIS:
               - Overall performance assessment
               - Strengths and accomplishments
               - Areas for improvement and practice
               - Specific skill development recommendations
               - Follow-up action items and timeline
            
            6. SCENARIO VARIATIONS:
               - Panel interview dynamics
               - Phone vs video vs in-person formats
               - Stress interview techniques
               - Case study presentations
               - Technical whiteboarding sessions
               - Culture fit conversations
            
            Provide immersive simulation with detailed performance feedback.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="question_generator",
                description="Generate comprehensive interview questions categorized by type and difficulty level",
                func=question_generator
            ),
            Tool(
                name="answer_coach",
                description="Provide detailed coaching for interview answer improvement and delivery",
                func=answer_coach
            ),
            Tool(
                name="company_research_analyst",
                description="Analyze companies and roles for strategic interview preparation",
                func=company_research_analyst
            ),
            Tool(
                name="mock_interview_simulator",
                description="Simulate realistic interview scenarios with comprehensive feedback",
                func=mock_interview_simulator
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create LangChain agent for comprehensive interview preparation"""
        
        system_prompt = """
        You are an expert AI Interview Coach with access to powerful preparation tools.
        
        Your expertise encompasses:
        - Interview question generation and categorization
        - Answer coaching and delivery improvement
        - Company research and strategic positioning
        - Mock interview simulation and feedback
        - Comprehensive interview preparation strategies
        
        Core principles for interview coaching:
        
        1. COMPREHENSIVE PREPARATION: Cover all aspects from questions to company research
        2. PRACTICAL SIMULATION: Provide realistic practice opportunities with feedback
        3. STRATEGIC POSITIONING: Help candidates align strengths with role requirements
        4. CONFIDENCE BUILDING: Reduce anxiety through thorough preparation and practice
        5. AUTHENTIC PRESENTATION: Maintain genuineness while optimizing presentation
        
        When providing interview preparation:
        1. Assess candidate's experience level and target role
        2. Use specialized tools for comprehensive preparation strategy
        3. Provide specific, actionable improvement recommendations
        4. Simulate realistic interview scenarios and conditions
        5. Build confidence through thorough preparation and practice
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def get_interview_questions(self, role: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Get comprehensive interview preparation using LangChain agent"""
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items() if v])
            enhanced_query = f"""
            INTERVIEW CONTEXT:
            {context_str}
            
            TARGET ROLE:
            {role}
            
            Please provide comprehensive interview preparation including questions, coaching, and strategic guidance.
            """
        else:
            enhanced_query = f"Generate challenging and relevant mock interview questions and preparation strategy for the role: {role}"
        
        try:
            response = self.agent_executor.invoke({"input": enhanced_query})
            return response["output"]
        
        except Exception as e:
            # Fallback to direct LLM call
            fallback_prompt = f"""
            As an expert interview coach, provide comprehensive preparation for:
            Role: {role}
            
            Include:
            - Relevant interview questions by category
            - Answer coaching and best practices
            - Company research strategies
            - Mock interview scenarios
            """
            
            try:
                fallback_response = self.llm.invoke([HumanMessage(content=fallback_prompt)])
                return fallback_response.content
            except Exception as fallback_error:
                return f"I apologize, but I'm experiencing technical difficulties. Please try again. Error: {str(fallback_error)}"

# Backward compatible function
def get_interview_questions(role: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Enhanced interview preparation with LangChain capabilities
    Backward compatible with existing code
    """
    if LANGCHAIN_AVAILABLE:
        try:
            agent = InterviewAgentLangChain()
            return agent.get_interview_questions(role, context)
        except Exception as e:
            print(f"[INFO] LangChain agent failed, falling back to simple completion: {e}")
    
    # Original implementation as fallback
    from utils.openai_helper import agentic_completion
    system_prompt = "You are an expert AI interviewer."
    user_prompt = f"Generate challenging and relevant mock interview questions for the role: {role}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
