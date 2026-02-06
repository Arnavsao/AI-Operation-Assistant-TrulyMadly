"""
Planner Agent - Converts user input into structured execution plan
"""
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from llm.client import LLMClient
from tools.base import BaseTool


class ExecutionStep(BaseModel):
    """Single step in execution plan"""
    step_number: int = Field(description="Step number in sequence")
    tool_name: str = Field(description="Name of tool to use")
    parameters: Dict[str, Any] = Field(description="Parameters for tool execution")
    description: str = Field(description="Human-readable description of what this step does")


class ExecutionPlan(BaseModel):
    """Complete execution plan"""
    task_summary: str = Field(description="Summary of the user's task")
    steps: List[ExecutionStep] = Field(description="Ordered list of execution steps")
    expected_output: str = Field(description="Description of expected final output")


class PlannerAgent:
    """
    Planner Agent - Analyzes user request and creates structured execution plan
    """
    
    def __init__(self, llm_client: LLMClient, available_tools: List[BaseTool]):
        self.llm = llm_client
        self.tools = {tool.name: tool for tool in available_tools}
        self.tool_schemas = [tool.to_schema() for tool in available_tools]
    
    def create_plan(self, user_task: str) -> ExecutionPlan:
        """
        Create execution plan from user task
        
        Args:
            user_task: Natural language task description
            
        Returns:
            Structured execution plan
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(user_task)
        
        try:
            # Use LLM with structured output
            result = self.llm.generate_structured_output(
                prompt=user_prompt,
                system_prompt=system_prompt,
                response_format=ExecutionPlan,
                temperature=0.3  # Lower temperature for more deterministic planning
            )
            
            # Validate plan
            plan = ExecutionPlan(**result)
            self._validate_plan(plan)
            
            return plan
        except Exception as e:
            raise Exception(f"Planning failed: {str(e)}")
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with tool descriptions"""
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}\n  Parameters: {tool['parameters']}"
            for tool in self.tool_schemas
        ])
        
        return f"""You are a Planner Agent in an AI Operations Assistant system.

Your role is to analyze user requests and create a structured execution plan using available tools.

Available Tools:
{tools_description}

Instructions:
1. Understand the user's task and break it down into sequential steps
2. Select appropriate tools for each step
3. Specify exact parameters needed for each tool
4. Ensure steps are in logical order
5. Each step should have a clear purpose
6. The plan should be complete and executable

Output a structured JSON plan following the ExecutionPlan schema."""
    
    def _build_user_prompt(self, user_task: str) -> str:
        """Build user prompt"""
        return f"""User Task: {user_task}

Create a detailed execution plan to accomplish this task using the available tools.
Break down the task into clear, sequential steps."""
    
    def _validate_plan(self, plan: ExecutionPlan) -> None:
        """Validate that plan uses valid tools"""
        for step in plan.steps:
            if step.tool_name not in self.tools:
                raise ValueError(f"Invalid tool in plan: {step.tool_name}")
