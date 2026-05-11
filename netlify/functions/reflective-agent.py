import json
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI()

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    iterations: List[Dict[str, Any]]
    final_score: float
    history: List[Dict[str, str]]

def generate_initial_response(query: str) -> str:
    """Generate initial response"""
    user_lower = query.lower()
    
    if "code" in user_lower or "program" in user_lower:
        return "Here's a simple Python function to solve your problem:\n\n```python\ndef example():\n    return 'Hello, World!'\n```\n\nThis should get you started."
    elif "explain" in user_lower or "what is" in user_lower:
        return "Let me explain this concept to you. The basic idea is that it involves several key components working together to achieve a goal."
    elif "help" in user_lower or "assist" in user_lower:
        return "I'd be happy to help you with that. Here's what I can do: I can assist with questions, provide explanations, and offer guidance on various topics."
    else:
        return f"I've processed your request: '{query}'. Here's a general response that addresses your query based on the information provided."

def self_critique(response: str, query: str) -> Dict[str, Any]:
    """Critique the response"""
    score = 0.8
    issues = []
    suggestions = []
    
    if len(response) < 50:
        score -= 0.2
        issues.append("Response too short")
        suggestions.append("Add more detail")
    
    user_lower = query.lower()
    if "code" in user_lower and "```" not in response:
        score -= 0.15
        issues.append("Expected code but none provided")
        suggestions.append("Include code examples")
    elif "explain" in user_lower and len(response) < 100:
        score -= 0.15
        issues.append("Explanation lacks detail")
        suggestions.append("Provide more comprehensive explanation")
    
    return {
        "score": max(0.1, min(1.0, score)),
        "issues": issues,
        "suggestions": suggestions
    }

def improve_response(response: str, critique: Dict[str, Any], iteration: int) -> str:
    """Improve response based on critique"""
    improvements = []
    
    if "Response too short" in critique["issues"]:
        improvements.append("Adding more detailed information to provide a comprehensive response.")
    
    if "Expected code but none provided" in critique["issues"]:
        improvements.append(" Including code examples to demonstrate the concept.")
    
    if "Explanation lacks detail" in critique["issues"]:
        improvements.append("Expanding the explanation with more context and examples.")
    
    if not improvements:
        improvements.append("Refining the response for clarity and accuracy.")
    
    return response + "\n\n[Iteration " + str(iteration) + " Improvement]: " + " ".join(improvements)

def reflective_agent_response(user_message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Main reflective agent logic"""
    
    # 1. Generate initial response
    initial_response = generate_initial_response(user_message)
    
    # 2. Self-critique
    critique1 = self_critique(initial_response, user_message)
    
    # 3. First iteration
    iteration1_response = initial_response
    if critique1["score"] < 0.8:
        iteration1_response = improve_response(initial_response, critique1, 1)
    
    # 4. Second self-critique
    critique2 = self_critique(iteration1_response, user_message)
    
    # 5. Second iteration if needed
    final_response = iteration1_response
    if critique2["score"] < 0.75:
        final_response = improve_response(iteration1_response, critique2, 2)
    
    # Final critique
    final_critique = self_critique(final_response, user_message)
    
    iterations = [
        {"iteration": 1, "response": initial_response, "critique": critique1},
        {"iteration": 2, "response": iteration1_response, "critique": critique2}
    ]
    
    # Update history
    updated_history = history.copy()
    updated_history.append({"role": "user", "content": user_message})
    updated_history.append({"role": "assistant", "content": final_response})
    
    return {
        "response": final_response,
        "iterations": iterations,
        "final_score": final_critique["score"],
        "history": updated_history
    }

@app.get("/")
async def root():
    return {"message": "Reflective Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    try:
        result = reflective_agent_response(
            user_message=chat_message.message,
            history=chat_message.history or []
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)