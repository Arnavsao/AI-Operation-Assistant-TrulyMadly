"""
AI Operations Assistant - Main Application
FastAPI server with multi-agent orchestration using Google Gemini
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from llm.client import LLMClient
from tools import GitHubTool, WeatherTool, NewsTool
from agents import PlannerAgent, ExecutorAgent, VerifierAgent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Operations Assistant",
    description="Multi-agent AI system for task automation with Google Gemini LLM and API integrations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    llm_client = LLMClient()
    tools = [GitHubTool(), WeatherTool(), NewsTool()]
    
    planner = PlannerAgent(llm_client, tools)
    executor = ExecutorAgent(tools)
    verifier = VerifierAgent(llm_client)
except Exception as e:
    print(f"Error initializing components: {e}")
    print("Make sure all required environment variables are set in .env file")
    raise


# Request/Response models
class TaskRequest(BaseModel):
    """Request model for task execution"""
    task: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "task": "Find the top 3 Python machine learning repositories on GitHub and get the weather in San Francisco"
            }
        }


class TaskResponse(BaseModel):
    """Response model for task execution"""
    task_summary: str
    status: str
    results: Dict[str, Any]
    metadata: Dict[str, Any]
    execution_plan: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI Operations Assistant",
        "version": "1.0.0",
        "description": "Multi-agent AI system with Planner, Executor, and Verifier agents",
        "endpoints": {
            "/execute": "POST - Execute a natural language task",
            "/health": "GET - Health check",
            "/tools": "GET - List available tools"
        },
        "example_tasks": [
            "Find the top 5 Python repositories on GitHub",
            "Get the weather in Mumbai and London",
            "Find news about artificial intelligence",
            "Search for React repositories and get weather in New York",
            "Get technology news and find popular JavaScript projects"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": ["planner", "executor", "verifier"],
        "tools": [tool.name for tool in tools],
        "llm_model": llm_client.model_name
    }


@app.get("/tools")
async def list_tools():
    """List available tools and their descriptions"""
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in tools
        ]
    }


@app.post("/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """
    Execute a natural language task using multi-agent system
    
    Flow:
    1. Planner Agent creates execution plan
    2. Executor Agent runs each step
    3. Verifier Agent validates and formats results
    """
    try:
        # Step 1: Planning
        print(f"\n[PLANNER] Creating execution plan for: {request.task}")
        plan = planner.create_plan(request.task)
        print(f"[PLANNER] Created plan with {len(plan.steps)} steps")
        
        # Step 2: Execution
        print(f"\n[EXECUTOR] Executing {len(plan.steps)} steps...")
        step_results = executor.execute_plan(plan)
        
        for i, result in enumerate(step_results, 1):
            status = "✓" if result.success else "✗"
            print(f"[EXECUTOR] Step {i}/{len(plan.steps)} {status}: {result.step.description}")
        
        # Step 3: Verification
        print(f"\n[VERIFIER] Verifying results and formatting output...")
        final_output = verifier.verify_and_format(plan, step_results)
        print(f"[VERIFIER] Status: {final_output.status}, Quality: {final_output.metadata['quality_score']}/10")
        
        # Prepare response
        response = TaskResponse(
            task_summary=final_output.task_summary,
            status=final_output.status,
            results=final_output.results,
            metadata=final_output.metadata,
            execution_plan={
                "steps": [
                    {
                        "step_number": step.step_number,
                        "tool": step.tool_name,
                        "description": step.description,
                        "parameters": step.parameters
                    }
                    for step in plan.steps
                ],
                "expected_output": plan.expected_output
            }
        )
        
        print(f"\n[COMPLETE] Task finished with status: {final_output.status}\n")
        return response
        
    except Exception as e:
        print(f"\n[ERROR] Task execution failed: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("=" * 60)
    print("AI Operations Assistant - Multi-Agent System")
    print("=" * 60)
    print(f"Server starting on http://{host}:{port}")
    print(f"\nAvailable tools: {', '.join([tool.name for tool in tools])}")
    print(f"LLM Model: Google {llm_client.model_name}")
    print("\nExample request:")
    print('  curl -X POST http://localhost:8000/execute \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"task": "Find top 3 Python repos and get weather in Mumbai"}\'')
    print("=" * 60)
    print()
    
    uvicorn.run(app, host=host, port=port)
