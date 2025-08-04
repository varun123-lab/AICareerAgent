
"""
Enhanced Career Agent using LangChain Framework
Backward compatible with existing code while providing advanced capabilities
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

class CareerAgentLangChain:
    """Enhanced Career Agent using LangChain framework"""
    
    def __init__(self):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not installed. Install with: pip install langchain langchain-openai")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize memory for conversation context
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=5
        )
        
        # Create specialized tools
        self.tools = self._create_career_tools()
        
        # Create the agent
        self.agent_executor = self._create_agent()
    
    def _create_career_tools(self) -> List[Tool]:
        """Create career-specific tools for enhanced functionality"""
        
        def industry_trend_analyzer(industry_query: str) -> str:
            """Analyze current industry trends and market conditions"""
            prompt = f"""
            As a career market analyst, provide comprehensive industry analysis for: {industry_query}
            
            Include:
            1. Current market trends and growth outlook
            2. Emerging job roles and opportunities
            3. Skills in highest demand
            4. Salary ranges and compensation trends
            5. Remote work opportunities and policies
            6. Key companies and startups to watch
            7. Geographic job market hotspots
            8. Industry challenges and disruptions
            9. 2-5 year future predictions
            
            Provide specific, actionable insights for career planning.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def skill_development_planner(current_profile: str, target_role: str) -> str:
            """Create personalized skill development roadmap"""
            prompt = f"""
            Current Profile: {current_profile}
            Target Role: {target_role}
            
            Create a comprehensive skill development plan:
            
            1. CURRENT SKILL ASSESSMENT:
               - Transferable skills analysis
               - Strength identification
               - Experience relevance mapping
            
            2. SKILL GAP ANALYSIS:
               - Critical missing technical skills
               - Soft skills development needs
               - Industry-specific knowledge gaps
               - Certification requirements
            
            3. LEARNING ROADMAP (12-month plan):
               - Priority 1: Immediate focus (0-3 months)
               - Priority 2: Core development (3-6 months)
               - Priority 3: Advanced skills (6-9 months)
               - Priority 4: Specialization (9-12 months)
            
            4. PRACTICAL APPLICATION:
               - Portfolio project suggestions
               - Real-world practice opportunities
               - Open source contribution ideas
               - Networking and mentorship targets
            
            5. PROGRESS TRACKING:
               - Measurable milestones
               - Assessment checkpoints
               - Adjustment triggers
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def career_transition_strategist(transition_details: str) -> str:
            """Develop strategic career transition plan"""
            prompt = f"""
            Career Transition Context: {transition_details}
            
            Develop a strategic transition plan:
            
            1. TRANSITION FEASIBILITY:
               - Realistic timeline assessment
               - Risk analysis and mitigation
               - Financial planning considerations
               - Market opportunity evaluation
            
            2. POSITIONING STRATEGY:
               - Personal brand development
               - Resume/LinkedIn optimization
               - Portfolio and showcase creation
               - Storytelling for career change
            
            3. NETWORKING BLUEPRINT:
               - Target professional communities
               - Industry events and conferences
               - Informational interview strategy
               - Mentor identification approach
            
            4. JOB SEARCH TACTICS:
               - Company targeting strategy
               - Application optimization
               - Interview preparation specifics
               - Negotiation preparation
            
            5. EXECUTION TIMELINE:
               - Phase 1: Foundation building (months 1-3)
               - Phase 2: Active networking (months 2-4)
               - Phase 3: Job search execution (months 4-6)
               - Phase 4: Transition completion (months 6-8)
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def compensation_research_analyst(role_location_experience: str) -> str:
            """Provide detailed compensation analysis and negotiation strategy"""
            prompt = f"""
            Role/Location/Experience: {role_location_experience}
            
            Conduct comprehensive compensation analysis:
            
            1. MARKET RESEARCH:
               - Base salary ranges (25th, 50th, 75th, 90th percentiles)
               - Total compensation breakdown
               - Industry comparison analysis
               - Geographic adjustment factors
               - Experience level impact
            
            2. COMPENSATION COMPONENTS:
               - Base salary optimization
               - Bonus structure analysis
               - Equity/stock option evaluation
               - Benefits package assessment
               - Professional development allowances
               - Flexible work arrangements value
            
            3. NEGOTIATION STRATEGY:
               - Market positioning arguments
               - Value proposition development
               - Negotiation timing and tactics
               - Alternative compensation requests
               - Walk-away threshold determination
            
            4. LONG-TERM PLANNING:
               - Career progression salary trajectory
               - Performance review preparation
               - Promotion timeline strategy
               - External opportunity benchmarking
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="industry_trend_analyzer",
                description="Analyze current industry trends, market conditions, and future outlook for career planning",
                func=industry_trend_analyzer
            ),
            Tool(
                name="skill_development_planner",
                description="Create personalized skill development roadmaps with practical learning paths",
                func=skill_development_planner
            ),
            Tool(
                name="career_transition_strategist",
                description="Develop comprehensive career transition strategies with timeline and tactics",
                func=career_transition_strategist
            ),
            Tool(
                name="compensation_research_analyst",
                description="Provide detailed compensation analysis and negotiation strategies",
                func=compensation_research_analyst
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent with specialized career coaching capabilities"""
        
        system_prompt = """
        You are an expert AI Career Coach with access to powerful research and planning tools.
        
        Your expertise encompasses:
        - Industry trend analysis and market intelligence
        - Personalized skill development planning
        - Strategic career transition guidance
        - Compensation research and negotiation strategy
        - Professional networking and relationship building
        
        Core principles for providing career advice:
        
        1. TOOL-DRIVEN INSIGHTS: Always use your specialized tools to gather current, relevant data
        2. PERSONALIZATION: Tailor every recommendation to the individual's specific situation
        3. ACTIONABILITY: Provide concrete, specific steps with clear timelines
        4. STRATEGIC THINKING: Balance short-term tactics with long-term career vision
        5. MARKET AWARENESS: Ground advice in current market realities and trends
        
        When someone seeks career advice:
        1. Understand their current situation, goals, and constraints
        2. Use appropriate tools to research and analyze their specific context
        3. Synthesize insights into comprehensive, personalized guidance
        4. Provide prioritized action items with realistic timelines
        5. Address potential challenges and offer contingency planning
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
    
    def get_career_advice(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Get comprehensive career advice using LangChain agent and tools"""
        
        # Enhance query with context if provided
        if user_context:
            context_parts = []
            for key, value in user_context.items():
                if value:
                    context_parts.append(f"{key.replace('_', ' ').title()}: {value}")
            
            if context_parts:
                context_str = "\n".join(context_parts)
                enhanced_query = f"""
                PROFESSIONAL CONTEXT:
                {context_str}
                
                CAREER QUESTION:
                {query}
                
                Please provide comprehensive, personalized career guidance using your specialized tools.
                """
            else:
                enhanced_query = query
        else:
            enhanced_query = query
        
        try:
            response = self.agent_executor.invoke({"input": enhanced_query})
            return response["output"]
        
        except Exception as e:
            # Fallback to simple completion if agent fails
            fallback_prompt = f"""
            As an expert career coach, provide comprehensive advice for:
            
            {enhanced_query if 'enhanced_query' in locals() else query}
            
            Provide specific, actionable guidance that addresses their situation.
            """
            
            try:
                fallback_response = self.llm.invoke([HumanMessage(content=fallback_prompt)])
                return fallback_response.content
            except Exception as fallback_error:
                return f"I apologize, but I'm experiencing technical difficulties. Please try rephrasing your question. Error: {str(fallback_error)}"

# Backward compatible function - gradually migrate to this
def get_career_advice(query: str, user_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Enhanced career advice function with LangChain capabilities
    Backward compatible with existing code
    """
    if LANGCHAIN_AVAILABLE:
        try:
            # Use enhanced LangChain agent
            agent = CareerAgentLangChain()
            return agent.get_career_advice(query, user_context)
        except Exception as e:
            print(f"[INFO] LangChain agent failed, falling back to simple completion: {e}")
            # Fallback to original implementation
            pass
    
    # Original implementation as fallback
    from utils.openai_helper import agentic_completion
    system_prompt = "You are an expert AI career coach with deep industry knowledge and practical experience."
    user_prompt = f"Give detailed, personalized career advice for: {query}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]