"""
Executor Agent - Executes planned steps and calls tools
"""
from typing import Any, Dict, List
from tools.base import BaseTool
from agents.planner import ExecutionPlan, ExecutionStep


class StepResult:
    """Result of executing a single step"""
    
    def __init__(self, step: ExecutionStep, success: bool, data: Any = None, error: str = None):
        self.step = step
        self.success = success
        self.data = data
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "step_number": self.step.step_number,
            "tool_name": self.step.tool_name,
            "description": self.step.description,
            "success": self.success,
            "data": self.data,
            "error": self.error
        }


class ExecutorAgent:
    """
    Executor Agent - Executes planned steps and manages tool calls
    """
    
    def __init__(self, available_tools: List[BaseTool]):
        self.tools = {tool.name: tool for tool in available_tools}
        self.max_retries = 2
    
    def execute_plan(self, plan: ExecutionPlan) -> List[StepResult]:
        """
        Execute all steps in the plan
        
        Args:
            plan: Execution plan from Planner Agent
            
        Returns:
            List of step results
        """
        results = []
        
        for step in plan.steps:
            result = self._execute_step(step)
            results.append(result)
            
            # If a critical step fails, we might want to stop
            # For now, we continue to gather all results
        
        return results
    
    def _execute_step(self, step: ExecutionStep) -> StepResult:
        """
        Execute a single step with retry logic
        
        Args:
            step: Execution step
            
        Returns:
            Step result
        """
        tool = self.tools.get(step.tool_name)
        
        if not tool:
            return StepResult(
                step=step,
                success=False,
                error=f"Tool '{step.tool_name}' not found"
            )
        
        # Try executing with retries
        last_error = None
        for attempt in range(self.max_retries):
            try:
                result = tool.execute(**step.parameters)
                
                if result.get("success"):
                    return StepResult(
                        step=step,
                        success=True,
                        data=result.get("data")
                    )
                else:
                    last_error = result.get("error", "Unknown error")
                    # If it's a client error (like invalid city), don't retry
                    if "not found" in last_error.lower():
                        break
            except Exception as e:
                last_error = str(e)
        
        return StepResult(
            step=step,
            success=False,
            error=last_error or "Execution failed after retries"
        )
