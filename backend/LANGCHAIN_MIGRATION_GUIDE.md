# 🚀 LangChain Migration Guide for AI Career Agent

## Why Migrate to LangChain?

Your current implementation is great, but LangChain offers powerful advantages:

### Current Approach (Simple OpenAI calls):
```python
def get_career_advice(query):
    system_prompt = "You are an expert AI career coach."
    user_prompt = f"Give detailed, personalized career advice for: {query}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
```

### LangChain Approach Benefits:
- 🧰 **Tools Integration**: Agents can use external APIs, databases, web search
- 🧠 **Memory**: Maintain conversation context across interactions
- 🔄 **Chain of Thought**: Multi-step reasoning and planning
- 📊 **Structured Output**: Better data handling and parsing
- 🔧 **Extensibility**: Easy to add new capabilities
- 🎯 **Specialized Agents**: Different agents for different tasks

## Migration Steps

### Step 1: Install Dependencies
```bash
cd /Users/varunbarmavat/Desktop/AICareerAgent/backend
pip install -r requirements.txt
```

### Step 2: Create LangChain Agent Helper
Create `utils/langchain_helper.py`:

```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage
from langchain.memory import ConversationBufferWindowMemory

class BaseLangChainAgent:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=5
        )
    
    def create_agent(self, system_prompt: str, tools: list = None):
        if tools is None:
            tools = []
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        if tools:
            agent = create_openai_functions_agent(
                llm=self.llm,
                tools=tools,
                prompt=prompt
            )
            return AgentExecutor(
                agent=agent,
                tools=tools,
                memory=self.memory,
                verbose=True
            )
        else:
            # Simple completion without tools
            return self.llm
```

### Step 3: Migrate Individual Agents

#### Career Agent Migration:

**Before (current):**
```python
def get_career_advice(query):
    system_prompt = "You are an expert AI career coach."
    user_prompt = f"Give detailed, personalized career advice for: {query}"
    result = agentic_completion(system_prompt, user_prompt)
    return result["content"]
```

**After (LangChain):**
```python
from utils.langchain_helper import BaseLangChainAgent
from langchain.tools import Tool

class CareerAgent(BaseLangChainAgent):
    def __init__(self):
        super().__init__()
        self.tools = self._create_tools()
        self.agent_executor = self.create_agent(
            system_prompt="""You are an expert AI career coach with access to specialized tools.
            Use your tools to provide comprehensive, data-driven career advice.""",
            tools=self.tools
        )
    
    def _create_tools(self):
        def salary_research(role_and_location: str) -> str:
            # Could integrate with Glassdoor API, LinkedIn API, etc.
            prompt = f"Research current salary ranges for: {role_and_location}"
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        def skill_trends_analysis(industry: str) -> str:
            prompt = f"Analyze current skill trends and demand in: {industry}"
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        
        return [
            Tool(name="salary_research", description="Research salary ranges for specific roles", func=salary_research),
            Tool(name="skill_trends", description="Analyze industry skill trends", func=skill_trends_analysis)
        ]
    
    def get_career_advice(self, query: str) -> str:
        response = self.agent_executor.invoke({"input": query})
        return response["output"]
```

### Step 4: Update Flask Routes

**Before:**
```python
@app.route("/career-advice", methods=["POST"])
def career_advice():
    data = request.get_json()
    query = data.get("query", "")
    result = get_career_advice(query)
    return jsonify({"advice": result})
```

**After:**
```python
from agents.career_agent_langchain import CareerAgent

# Initialize agent once (or use singleton pattern)
career_agent = CareerAgent()

@app.route("/career-advice", methods=["POST"])
def career_advice():
    data = request.get_json()
    query = data.get("query", "")
    
    # Optional: Include user context
    user_context = {
        "experience_level": data.get("experience", ""),
        "current_role": data.get("current_role", ""),
        "industry": data.get("industry", "")
    }
    
    # Enhanced query with context
    if any(user_context.values()):
        context_str = ", ".join([f"{k}: {v}" for k, v in user_context.items() if v])
        enhanced_query = f"Context: {context_str}. Question: {query}"
    else:
        enhanced_query = query
    
    result = career_agent.get_career_advice(enhanced_query)
    return jsonify({"advice": result})
```

## Advanced Features You Can Add

### 1. Multi-Agent Conversation
```python
class CareerAdvisorTeam:
    def __init__(self):
        self.career_agent = CareerAgent()
        self.resume_agent = ResumeAgent()
        self.interview_agent = InterviewAgent()
        self.learning_agent = LearningAgent()
    
    def comprehensive_career_plan(self, user_profile: dict) -> dict:
        # Coordinate between multiple agents
        career_advice = self.career_agent.get_advice(user_profile)
        resume_tips = self.resume_agent.optimize_resume(user_profile)
        interview_prep = self.interview_agent.prepare_interview(user_profile)
        learning_path = self.learning_agent.create_learning_plan(user_profile)
        
        return {
            "career_strategy": career_advice,
            "resume_optimization": resume_tips,
            "interview_preparation": interview_prep,
            "learning_roadmap": learning_path
        }
```

### 2. Memory and Context Preservation
```python
class ContextAwareCareerAgent(CareerAgent):
    def get_career_advice(self, query: str, session_id: str = None) -> str:
        # Memory persists across conversation
        if session_id:
            self.memory.session_id = session_id
        
        response = self.agent_executor.invoke({"input": query})
        return response["output"]
```

### 3. External Tool Integration
```python
def create_external_tools():
    def job_search_api(query: str) -> str:
        # Integrate with Indeed, LinkedIn, etc.
        pass
    
    def salary_data_api(role: str, location: str) -> str:
        # Integrate with Glassdoor, PayScale, etc.
        pass
    
    def skill_assessment_api(skills: str) -> str:
        # Integrate with skill testing platforms
        pass
    
    return [
        Tool(name="job_search", description="Search current job openings", func=job_search_api),
        Tool(name="salary_data", description="Get real salary data", func=salary_data_api),
        Tool(name="skill_assessment", description="Assess skill levels", func=skill_assessment_api)
    ]
```

## Implementation Timeline

### Phase 1 (Week 1): Basic Migration
- [ ] Install LangChain dependencies
- [ ] Create base agent helper class
- [ ] Migrate one agent (career_agent) to LangChain
- [ ] Test basic functionality

### Phase 2 (Week 2): Enhanced Features
- [ ] Add tools to agents
- [ ] Implement memory and context
- [ ] Migrate remaining agents
- [ ] Update frontend to handle richer responses

### Phase 3 (Week 3): Advanced Features
- [ ] Multi-agent coordination
- [ ] External API integrations
- [ ] Advanced prompt engineering
- [ ] Performance optimization

## Testing Your Migration

1. **Test Basic Functionality:**
```python
# Test file: test_langchain_migration.py
from agents.career_agent_langchain import CareerAgent

def test_career_agent():
    agent = CareerAgent()
    response = agent.get_career_advice("I want to transition from marketing to data science")
    print(response)
    assert len(response) > 0
```

2. **Compare Responses:**
```python
# Compare old vs new implementation
old_response = get_career_advice_old("career question")
new_response = career_agent.get_career_advice("career question")

print("Old:", old_response)
print("New:", new_response)
```

## Benefits You'll Get

1. **Smarter Responses**: Agents can use tools to get real data
2. **Better Context**: Memory maintains conversation flow
3. **Extensibility**: Easy to add new capabilities
4. **Reliability**: Better error handling and retries
5. **Performance**: Optimized for complex reasoning tasks

Would you like me to help you implement any specific part of this migration?
