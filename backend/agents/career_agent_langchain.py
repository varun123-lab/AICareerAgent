"""
LangChain-powered Career Agent
A drop-in replacement for the current career_agent.py with enhanced capabilities
"""

import os
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage
from langchain.memory import ConversationBufferWindowMemory

class CareerAgentLangChain:
    """Enhanced Career Agent using LangChain framework"""
    
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
            k=5  # Remember last 5 exchanges
        )
        
        # Create specialized tools
        self.tools = self._create_career_tools()
        
        # Create the agent
        self.agent_executor = self._create_agent()
    
    def _create_career_tools(self) -> List[Tool]:
        """Create career-specific tools for the agent"""
        
        def industry_analysis(industry_query: str) -> str:
            """Analyze industry trends, growth prospects, and opportunities"""
            prompt = f"""
            As a career market analyst, provide comprehensive analysis for: {industry_query}
            
            Include:
            1. Current industry trends and growth projections
            2. Emerging roles and opportunities
            3. Skills in high demand
            4. Salary expectations and ranges
            5. Key companies and employers
            6. Geographic hotspots for opportunities
            7. Potential challenges and risks
            8. Future outlook (2-5 years)
            
            Be specific and data-driven in your analysis.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def skill_roadmap_creator(current_background: str, target_role: str) -> str:
            """Create detailed skill development roadmap"""
            prompt = f"""
            Current Background: {current_background}
            Target Role: {target_role}
            
            Create a detailed skill development roadmap including:
            
            1. SKILL AUDIT:
               - Skills you already have that transfer
               - Current skill level assessment
            
            2. SKILL GAPS:
               - Technical skills missing
               - Soft skills to develop
               - Certifications needed
            
            3. LEARNING PATH (prioritized):
               - Immediate focus (0-3 months)
               - Short-term goals (3-6 months)
               - Medium-term objectives (6-12 months)
               - Long-term development (1-2 years)
            
            4. RESOURCES:
               - Specific courses, books, tutorials
               - Practice projects and portfolios
               - Networking opportunities
               - Mentorship suggestions
            
            5. MILESTONES:
               - Measurable progress indicators
               - Portfolio project suggestions
               - Achievement timeline
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def career_transition_planner(current_role: str, desired_role: str, constraints: str = "") -> str:
            """Plan strategic career transition with realistic timeline"""
            prompt = f"""
            Current Role: {current_role}
            Desired Role: {desired_role}
            Constraints/Considerations: {constraints}
            
            Create a strategic career transition plan:
            
            1. TRANSITION ASSESSMENT:
               - Feasibility analysis
               - Timeline estimate
               - Potential challenges
               - Risk mitigation strategies
            
            2. BRIDGE STRATEGIES:
               - Intermediate roles to consider
               - Internal transition opportunities
               - Side projects to build credibility
               - Networking strategies
            
            3. TIMELINE BREAKDOWN:
               - Phase 1: Preparation (skills, portfolio)
               - Phase 2: Positioning (networking, applications)
               - Phase 3: Transition (job search, interviews)
               - Phase 4: Integration (first 90 days in new role)
            
            4. ACTION ITEMS:
               - Immediate next steps (this week)
               - 30-day goals
               - 90-day milestones
               - 6-month objectives
            
            5. SUCCESS METRICS:
               - How to measure progress
               - Key performance indicators
               - Adjustment triggers
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def compensation_advisor(role: str, location: str, experience: str) -> str:
            """Provide compensation guidance and negotiation strategies"""
            prompt = f"""
            Role: {role}
            Location: {location}
            Experience Level: {experience}
            
            Provide comprehensive compensation guidance:
            
            1. SALARY RESEARCH:
               - Base salary ranges (low, median, high)
               - Total compensation breakdown
               - Industry benchmarks
               - Location-adjusted ranges
            
            2. COMPENSATION COMPONENTS:
               - Base salary
               - Bonus structures
               - Equity/stock options
               - Benefits package value
               - Professional development allowances
            
            3. NEGOTIATION STRATEGY:
               - Research preparation
               - Timing considerations
               - Negotiation talking points
               - Alternative compensation requests
               - Red lines and walk-away points
            
            4. MARKET POSITIONING:
               - How to position your value
               - Unique selling propositions
               - Quantifiable achievements to highlight
               - Competitive analysis
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def networking_strategist(career_goal: str, current_network: str = "limited") -> str:
            """Develop strategic networking plan for career advancement"""
            prompt = f"""
            Career Goal: {career_goal}
            Current Network Status: {current_network}
            
            Create a strategic networking plan:
            
            1. NETWORK MAPPING:
               - Target personas to connect with
               - Key industry events and conferences
               - Professional associations to join
               - Online communities and platforms
            
            2. NETWORKING TACTICS:
               - LinkedIn optimization strategies
               - Informational interview approaches
               - Value-first networking methods
               - Follow-up and relationship building
            
            3. CONTENT STRATEGY:
               - Thought leadership topics
               - Social media presence building
               - Professional writing opportunities
               - Speaking and presentation opportunities
            
            4. RELATIONSHIP BUILDING:
               - Mentor identification and approach
               - Peer connection strategies
               - Industry influencer engagement
               - Alumni network activation
            
            5. NETWORKING SCHEDULE:
               - Daily networking activities (15-30 min)
               - Weekly networking goals
               - Monthly networking events
               - Quarterly relationship review
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="industry_analysis",
                description="Analyze industry trends, growth prospects, and career opportunities in specific sectors",
                func=industry_analysis
            ),
            Tool(
                name="skill_roadmap_creator",
                description="Create detailed skill development roadmaps for career transitions",
                func=skill_roadmap_creator
            ),
            Tool(
                name="career_transition_planner",
                description="Plan strategic career transitions with realistic timelines and actionable steps",
                func=career_transition_planner
            ),
            Tool(
                name="compensation_advisor",
                description="Provide salary research and negotiation strategies for specific roles and locations",
                func=compensation_advisor
            ),
            Tool(
                name="networking_strategist",
                description="Develop strategic networking plans for career advancement and opportunity creation",
                func=networking_strategist
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent with specialized career coaching capabilities"""
        
        system_prompt = """
        You are an expert AI Career Coach with access to specialized research and planning tools.
        
        Your expertise includes:
        - Industry analysis and market research
        - Skill development planning and roadmapping
        - Strategic career transition planning
        - Compensation research and negotiation
        - Professional networking strategies
        - Personal branding and positioning
        
        Guidelines for providing career advice:
        
        1. ALWAYS use relevant tools to provide data-driven, researched advice
        2. Personalize recommendations based on the user's specific situation
        3. Provide actionable, specific guidance with clear next steps
        4. Consider both short-term tactics and long-term strategy
        5. Address potential challenges and provide mitigation strategies
        6. Be encouraging while being realistic about timelines and challenges
        7. Focus on building sustainable career momentum
        
        When someone asks for career advice:
        1. First understand their current situation and goals
        2. Use appropriate tools to gather relevant information
        3. Synthesize tool outputs into comprehensive, personalized advice
        4. Provide specific action items and timelines
        5. Offer to dive deeper into any specific area
        
        Always aim to provide value that goes beyond generic career advice.
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
        """
        Get comprehensive career advice using LangChain agent and tools
        
        Args:
            query: User's career question or goal
            user_context: Optional context like current role, skills, experience level, location
            
        Returns:
            Comprehensive career advice with actionable recommendations
        """
        
        # Enhance query with context if provided
        if user_context:
            context_parts = []
            for key, value in user_context.items():
                if value:  # Only include non-empty values
                    context_parts.append(f"{key.replace('_', ' ').title()}: {value}")
            
            if context_parts:
                context_str = "\n".join(context_parts)
                enhanced_query = f"""
                CONTEXT:
                {context_str}
                
                QUESTION:
                {query}
                """
            else:
                enhanced_query = query
        else:
            enhanced_query = query
        
        try:
            response = self.agent_executor.invoke({
                "input": enhanced_query
            })
            return response["output"]
        
        except Exception as e:
            # Fallback to simple completion if agent fails
            fallback_prompt = f"""
            As an expert career coach, provide helpful advice for this career question:
            
            {enhanced_query if 'enhanced_query' in locals() else query}
            
            Provide specific, actionable advice that addresses their situation.
            """
            
            try:
                fallback_response = self.llm.invoke([HumanMessage(content=fallback_prompt)])
                return fallback_response.content
            except Exception as fallback_error:
                return f"I apologize, but I'm experiencing technical difficulties. Please try rephrasing your question or try again later. Error: {str(fallback_error)}"


# Drop-in replacement function for existing code
def get_career_advice_langchain(query: str, user_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Drop-in replacement for existing get_career_advice function with LangChain enhancements
    
    This function maintains compatibility with existing code while providing enhanced capabilities
    """
    # Initialize agent (in production, you'd want to use singleton pattern or global instance)
    agent = CareerAgentLangChain()
    return agent.get_career_advice(query, user_context)


# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced career agent
    agent = CareerAgentLangChain()
    
    # Example 1: Basic career advice
    response1 = agent.get_career_advice("I'm a marketing manager wanting to transition to product management")
    print("Response 1:", response1)
    
    # Example 2: Career advice with context
    user_context = {
        "current_role": "Marketing Manager",
        "experience_years": "5",
        "industry": "SaaS",
        "location": "San Francisco",
        "education": "MBA"
    }
    
    response2 = agent.get_career_advice(
        "What steps should I take to become a Senior Product Manager?", 
        user_context
    )
    print("Response 2:", response2)
