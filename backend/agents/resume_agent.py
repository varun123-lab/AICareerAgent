
"""
Enhanced Resume Agent using LangChain Framework
Advanced resume optimization with specialized tools and analysis
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

class ResumeAgentLangChain:
    """Enhanced Resume Agent using LangChain framework"""
    
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
            k=3
        )
        
        self.tools = self._create_resume_tools()
        self.agent_executor = self._create_agent()
    
    def _create_resume_tools(self) -> List[Tool]:
        """Create resume-specific tools for advanced optimization"""
        
        def ats_optimizer(content: str) -> str:
            """Optimize content for Applicant Tracking Systems (ATS)"""
            prompt = f"""
            As an ATS optimization expert, analyze and improve this resume content: {content}
            
            Provide ATS-optimized recommendations:
            
            1. KEYWORD OPTIMIZATION:
               - Industry-relevant keywords to include
               - Technical skills to highlight
               - Action verbs that score well
               - Certification and qualification terms
            
            2. FORMAT RECOMMENDATIONS:
               - ATS-friendly section headers
               - Proper use of bullet points
               - Date format optimization
               - Contact information best practices
            
            3. CONTENT STRUCTURE:
               - Skills section organization
               - Experience description improvements
               - Education section optimization
               - Quantifiable achievements emphasis
            
            4. COMMON ATS PITFALLS TO AVOID:
               - Formatting issues that cause parsing errors
               - Graphics and design elements to avoid
               - File format recommendations
               - Character and symbol usage guidelines
            
            Provide specific, actionable improvements.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def achievement_quantifier(experience_text: str) -> str:
            """Transform experience into quantified, achievement-focused bullet points"""
            prompt = f"""
            Transform this experience into powerful, quantified resume bullets: {experience_text}
            
            Apply the STAR method (Situation, Task, Action, Result) and follow these principles:
            
            1. QUANTIFICATION FOCUS:
               - Include specific numbers, percentages, dollar amounts
               - Mention team sizes, project scopes, timelines
               - Show before/after improvements
               - Highlight growth metrics and impact
            
            2. ACTION VERB OPTIMIZATION:
               - Start with strong, varied action verbs
               - Use industry-specific terminology
               - Demonstrate leadership and initiative
               - Show progression and responsibility growth
            
            3. IMPACT DEMONSTRATION:
               - Business value and ROI
               - Process improvements and efficiency gains
               - Customer satisfaction and retention metrics
               - Revenue generation and cost savings
            
            4. TECHNICAL SKILL INTEGRATION:
               - Relevant technologies and tools
               - Methodologies and frameworks
               - Certifications and standards applied
               - Cross-functional collaboration
            
            Generate 3-5 powerful bullet points that showcase measurable achievements.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def skills_matrix_builder(role_target: str, current_skills: str) -> str:
            """Build comprehensive skills matrix aligned with target role"""
            prompt = f"""
            Target Role: {role_target}
            Current Skills: {current_skills}
            
            Build a comprehensive skills matrix:
            
            1. TECHNICAL SKILLS ASSESSMENT:
               - Core technical requirements for target role
               - Programming languages and frameworks
               - Tools and software proficiency levels
               - Cloud platforms and infrastructure knowledge
               - Database and data management skills
            
            2. SOFT SKILLS MATRIX:
               - Leadership and management capabilities
               - Communication and presentation skills
               - Problem-solving and analytical thinking
               - Project management and organization
               - Adaptability and learning agility
            
            3. INDUSTRY-SPECIFIC SKILLS:
               - Domain knowledge requirements
               - Regulatory and compliance understanding
               - Industry tools and methodologies
               - Market trends and competitive knowledge
               - Customer or user experience focus
            
            4. SKILL PRIORITIZATION:
               - Must-have skills for role qualification
               - Nice-to-have skills for competitive advantage
               - Emerging skills for future growth
               - Transferable skills from current experience
            
            5. RESUME PRESENTATION:
               - How to categorize and present skills
               - Proficiency level indicators
               - Context and application examples
               - Skill validation through experience
            
            Provide a structured skills matrix with clear recommendations.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def resume_section_optimizer(section_content: str, section_type: str) -> str:
            """Optimize specific resume sections with targeted improvements"""
            prompt = f"""
            Section Type: {section_type}
            Current Content: {section_content}
            
            Provide section-specific optimization:
            
            PROFESSIONAL SUMMARY OPTIMIZATION:
            - 3-4 line compelling value proposition
            - Key achievements and years of experience
            - Core competencies and unique strengths
            - Career trajectory and aspirations
            
            EXPERIENCE SECTION OPTIMIZATION:
            - Company/role context and significance
            - Scope of responsibility and team leadership
            - Key projects and strategic initiatives
            - Quantified results and business impact
            
            EDUCATION SECTION OPTIMIZATION:
            - Relevant coursework and academic projects
            - GPA inclusion guidelines (when appropriate)
            - Academic honors and achievements
            - Extracurricular leadership roles
            
            SKILLS SECTION OPTIMIZATION:
            - Technical skills categorization
            - Proficiency level indicators
            - Industry-relevant tool expertise
            - Certification and training highlights
            
            PROJECTS SECTION OPTIMIZATION:
            - Project scope and technical complexity
            - Technologies and methodologies used
            - Team collaboration and leadership role
            - Business value and user impact
            
            Provide specific, actionable improvements for the {section_type} section.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="ats_optimizer",
                description="Optimize resume content for Applicant Tracking Systems (ATS) compatibility and keyword ranking",
                func=ats_optimizer
            ),
            Tool(
                name="achievement_quantifier",
                description="Transform experience descriptions into quantified, achievement-focused bullet points",
                func=achievement_quantifier
            ),
            Tool(
                name="skills_matrix_builder",
                description="Build comprehensive skills matrix aligned with target role requirements",
                func=skills_matrix_builder
            ),
            Tool(
                name="resume_section_optimizer",
                description="Optimize specific resume sections with targeted improvements and best practices",
                func=resume_section_optimizer
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create LangChain agent for comprehensive resume optimization"""
        
        system_prompt = """
        You are an expert AI Resume Strategist with access to powerful optimization tools.
        
        Your expertise encompasses:
        - ATS (Applicant Tracking System) optimization
        - Achievement quantification and impact demonstration
        - Skills matrix development and alignment
        - Section-specific optimization strategies
        - Industry-specific resume best practices
        
        Core principles for resume optimization:
        
        1. RESULTS-DRIVEN: Focus on quantified achievements and business impact
        2. ATS-OPTIMIZED: Ensure compatibility with modern hiring systems
        3. ROLE-ALIGNED: Tailor content to specific job requirements
        4. COMPETITIVE: Position candidate advantageously against competition
        5. AUTHENTIC: Maintain accuracy while maximizing presentation impact
        
        When optimizing resumes:
        1. Analyze current content and identify improvement opportunities
        2. Use specialized tools for targeted optimization
        3. Provide specific, actionable recommendations
        4. Consider both human readers and ATS systems
        5. Ensure consistency and professional presentation
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
    
    def generate_resume_bullets(self, experience: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate optimized resume bullet points using LangChain agent"""
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items() if v])
            enhanced_query = f"""
            CONTEXT:
            {context_str}
            
            EXPERIENCE TO OPTIMIZE:
            {experience}
            
            Please generate powerful, quantified resume bullet points that will perform well in ATS systems and impress hiring managers.
            """
        else:
            enhanced_query = f"Generate strong, achievement-focused resume bullet points for this experience: {experience}"
        
        try:
            response = self.agent_executor.invoke({"input": enhanced_query})
            return response["output"]
        
        except Exception as e:
            # Fallback to direct LLM call
            fallback_prompt = f"""
            As an expert resume writer, create powerful bullet points for:
            {experience}
            
            Focus on:
            - Quantified achievements
            - Strong action verbs
            - Business impact
            - ATS-friendly keywords
            """
            
            try:
                fallback_response = self.llm.invoke([HumanMessage(content=fallback_prompt)])
                return fallback_response.content
            except Exception as fallback_error:
                return f"I apologize, but I'm experiencing technical difficulties. Please try again. Error: {str(fallback_error)}"

# Backward compatible function
def generate_resume_bullets(experience: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Enhanced resume bullet generation with LangChain capabilities
    Backward compatible with existing code
    """
    if LANGCHAIN_AVAILABLE:
        try:
            agent = ResumeAgentLangChain()
            return agent.generate_resume_bullets(experience, context)
        except Exception as e:
            print(f"[INFO] LangChain agent failed, falling back to simple completion: {e}")
    
    # Original implementation as fallback
    from utils.openai_helper import agentic_completion
    system_prompt = "You are an expert AI resume writer."
    user_prompt = f"Generate strong, achievement-focused resume bullet points for this experience: {experience}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
