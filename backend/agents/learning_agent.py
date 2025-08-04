
"""
Enhanced Learning Agent using LangChain Framework
Comprehensive learning resource discovery and pathway planning
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

class LearningAgentLangChain:
    """Enhanced Learning Agent using LangChain framework"""
    
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
        
        self.tools = self._create_learning_tools()
        self.agent_executor = self._create_agent()
    
    def _create_learning_tools(self) -> List[Tool]:
        """Create learning-specific tools for comprehensive resource discovery"""
        
        def learning_pathway_architect(topic_goal: str) -> str:
            """Design structured learning pathways with progression levels"""
            prompt = f"""
            Topic/Goal: {topic_goal}
            
            Design a comprehensive learning pathway:
            
            1. SKILL LEVEL ASSESSMENT:
               - Beginner fundamentals checklist
               - Intermediate knowledge requirements
               - Advanced mastery indicators
               - Expert-level specializations
            
            2. STRUCTURED LEARNING PATH:
               - Foundation Phase (0-3 months):
                 * Core concepts and terminology
                 * Essential tools and environment setup
                 * Basic hands-on projects
                 * Recommended beginner resources
               
               - Development Phase (3-6 months):
                 * Intermediate concepts and applications
                 * Real-world project experience
                 * Best practices and design patterns
                 * Community engagement opportunities
               
               - Mastery Phase (6-12 months):
                 * Advanced techniques and optimization
                 * Complex project development
                 * Teaching and mentoring others
                 * Industry contribution opportunities
            
            3. LEARNING MILESTONES:
               - Knowledge checkpoints
               - Practical application markers
               - Portfolio development goals
               - Certification targets
            
            4. RESOURCE ALLOCATION:
               - Time investment recommendations
               - Cost-benefit analysis of paid resources
               - Free vs premium learning options
               - Study schedule optimization
            
            Provide a clear, actionable learning roadmap.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def resource_curator(topic_criteria: str) -> str:
            """Curate high-quality learning resources across multiple formats"""
            prompt = f"""
            Learning Topic/Criteria: {topic_criteria}
            
            Curate comprehensive learning resources:
            
            1. ONLINE COURSES (MOOC Platforms):
               - Coursera top-rated courses with university partnerships
               - edX professional certificates and MicroMasters
               - Udacity Nanodegrees and industry partnerships
               - Pluralsight skill assessments and learning paths
               - LinkedIn Learning professional development
               
            2. INTERACTIVE LEARNING PLATFORMS:
               - Codecademy hands-on coding practice
               - freeCodeCamp project-based learning
               - Khan Academy foundational concepts
               - Brilliant problem-solving approach
               - LeetCode technical interview preparation
            
            3. BOOK RECOMMENDATIONS:
               - Foundational textbooks and theory
               - Practical guides and implementation
               - Industry case studies and examples
               - Recent publications and trends
               - Author credibility and expertise
            
            4. COMMUNITY AND NETWORKING:
               - Professional communities and forums
               - Discord/Slack learning groups
               - Local meetups and conferences
               - Mentorship and coaching opportunities
               - Open source contribution projects
            
            5. PRACTICAL APPLICATION:
               - GitHub project repositories for inspiration
               - Kaggle competitions and datasets
               - Personal project ideas and challenges
               - Industry collaboration opportunities
               - Portfolio development guidance
            
            6. QUALITY ASSESSMENT CRITERIA:
               - User ratings and completion rates
               - Industry recognition and accreditation
               - Instructor credentials and experience
               - Content freshness and relevance
               - Practical applicability and job market alignment
            
            Provide specific resource recommendations with quality indicators.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def skill_gap_analyzer(current_skills: str, target_role: str) -> str:
            """Analyze skill gaps and prioritize learning objectives"""
            prompt = f"""
            Current Skills: {current_skills}
            Target Role: {target_role}
            
            Conduct comprehensive skill gap analysis:
            
            1. CURRENT SKILL INVENTORY:
               - Technical skill assessment
               - Transferable skill identification
               - Experience depth evaluation
               - Certification and credential audit
            
            2. TARGET ROLE REQUIREMENTS:
               - Must-have technical skills
               - Preferred experience levels
               - Soft skill expectations
               - Industry knowledge requirements
               - Emerging skill trends
            
            3. GAP ANALYSIS MATRIX:
               - Critical missing skills (high priority)
               - Complementary skills (medium priority)
               - Nice-to-have skills (low priority)
               - Skill development timeline estimates
               - Resource investment requirements
            
            4. LEARNING PRIORITIZATION:
               - Quick wins (3-6 weeks)
               - Foundation building (2-3 months)
               - Advanced development (6-12 months)
               - Continuous learning areas
            
            5. VALIDATION STRATEGIES:
               - Self-assessment methods
               - Peer review opportunities
               - Professional evaluation options
               - Portfolio demonstration techniques
               - Interview preparation focus areas
            
            Provide actionable gap analysis with clear priorities.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def learning_progress_tracker(learning_context: str) -> str:
            """Create tracking system for learning progress and accountability"""
            prompt = f"""
            Learning Context: {learning_context}
            
            Design comprehensive progress tracking system:
            
            1. MILESTONE DEFINITION:
               - Knowledge acquisition checkpoints
               - Practical skill demonstration points
               - Project completion markers
               - Portfolio development stages
               - Certification achievement targets
            
            2. ASSESSMENT METHODS:
               - Self-evaluation questionnaires
               - Practical project assessments
               - Peer review and feedback
               - Mock interview simulations
               - Industry-standard evaluations
            
            3. TRACKING TOOLS AND SYSTEMS:
               - Learning journal templates
               - Progress visualization methods
               - Goal-setting frameworks (SMART goals)
               - Habit tracking applications
               - Portfolio documentation systems
            
            4. ACCOUNTABILITY MECHANISMS:
               - Study group participation
               - Mentor check-in schedules
               - Public commitment strategies
               - Progress sharing platforms
               - Learning community engagement
            
            5. ADAPTATION STRATEGIES:
               - Learning style optimization
               - Pace adjustment triggers
               - Resource substitution options
               - Goal modification protocols
               - Motivation maintenance techniques
            
            6. SUCCESS METRICS:
               - Knowledge retention indicators
               - Practical application success
               - Time-to-competency measurements
               - Career advancement correlation
               - Return on learning investment
            
            Provide actionable tracking framework with specific tools.
            """
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(
                name="learning_pathway_architect",
                description="Design structured learning pathways with clear progression levels and milestones",
                func=learning_pathway_architect
            ),
            Tool(
                name="resource_curator",
                description="Curate high-quality learning resources across multiple formats and platforms",
                func=resource_curator
            ),
            Tool(
                name="skill_gap_analyzer",
                description="Analyze skill gaps between current abilities and target role requirements",
                func=skill_gap_analyzer
            ),
            Tool(
                name="learning_progress_tracker",
                description="Create comprehensive tracking systems for learning progress and accountability",
                func=learning_progress_tracker
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create LangChain agent for comprehensive learning guidance"""
        
        system_prompt = """
        You are an expert AI Learning Strategist with access to powerful educational tools.
        
        Your expertise encompasses:
        - Learning pathway design and curriculum development
        - Resource curation and quality assessment
        - Skill gap analysis and prioritization
        - Progress tracking and accountability systems
        - Personalized learning optimization
        
        Core principles for learning guidance:
        
        1. PERSONALIZATION: Tailor learning paths to individual goals, experience, and constraints
        2. PRACTICAL FOCUS: Emphasize hands-on application and real-world projects
        3. QUALITY CURATION: Recommend only high-quality, validated learning resources
        4. PROGRESSIVE STRUCTURE: Design clear learning progressions from beginner to expert
        5. MEASURABLE OUTCOMES: Provide trackable milestones and assessment methods
        
        When providing learning guidance:
        1. Understand learner's current state, goals, and available time/resources
        2. Use specialized tools to design comprehensive learning strategies
        3. Provide specific resource recommendations with quality indicators
        4. Create actionable timelines and milestone markers
        5. Include accountability and progress tracking mechanisms
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
    
    def get_learning_resources(self, topic: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Get comprehensive learning resources using LangChain agent"""
        
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items() if v])
            enhanced_query = f"""
            LEARNING CONTEXT:
            {context_str}
            
            TOPIC TO LEARN:
            {topic}
            
            Please provide a comprehensive learning strategy including pathway design, resource curation, and progress tracking.
            """
        else:
            enhanced_query = f"Suggest the best learning strategy, resources, and pathway for mastering: {topic}"
        
        try:
            response = self.agent_executor.invoke({"input": enhanced_query})
            return response["output"]
        
        except Exception as e:
            # Fallback to direct LLM call
            fallback_prompt = f"""
            As an expert learning advisor, provide comprehensive guidance for learning:
            {topic}
            
            Include:
            - Structured learning pathway
            - High-quality resource recommendations
            - Practical application opportunities
            - Progress tracking methods
            """
            
            try:
                fallback_response = self.llm.invoke([HumanMessage(content=fallback_prompt)])
                return fallback_response.content
            except Exception as fallback_error:
                return f"I apologize, but I'm experiencing technical difficulties. Please try again. Error: {str(fallback_error)}"

# Backward compatible function
def get_learning_resources(topic: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Enhanced learning resource discovery with LangChain capabilities
    Backward compatible with existing code
    """
    if LANGCHAIN_AVAILABLE:
        try:
            agent = LearningAgentLangChain()
            return agent.get_learning_resources(topic, context)
        except Exception as e:
            print(f"[INFO] LangChain agent failed, falling back to simple completion: {e}")
    
    # Original implementation as fallback
    from utils.openai_helper import agentic_completion
    system_prompt = "You are an expert AI learning advisor."
    user_prompt = f"Suggest the best online resources, courses, and books for learning: {topic}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
