"""
Executor Agent - actually runs the steps and calls the APIs
Handles retries if something fails
"""
from typing import Any, Dict, List
from tools.base import BaseTool
from agents.planner import ExecutionPlan, ExecutionStep


class StepResult:
    """Stores what happened when we ran a step"""
    
    def __init__(self, step: ExecutionStep, success: bool, data: Any = None, error: str = None):
        self.step = step
        self.success = success
        self.data = data
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
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
    The worker - takes the plan and actually executes it
    Calls the right tools with the right parameters
    """
    
    def __init__(self, available_tools: List[BaseTool]):
        self.tools = {tool.name: tool for tool in available_tools}
        self.max_retries = 2  # Try twice if something fails
    
    def execute_plan(self, plan: ExecutionPlan) -> List[StepResult]:
        """
        Goes through each step in the plan and executes it
        Keeps going even if some steps fail (so we can see partial results)
        """
        results = []
        
        for step in plan.steps:
            result = self._execute_step(step)
            results.append(result)
        
        return results
    
    def _execute_step(self, step: ExecutionStep) -> StepResult:
        """
        Runs a single step - calls the tool with parameters
        Has retry logic in case of transient failures
        """
        tool = self.tools.get(step.tool_name)
        
        if not tool:
            return StepResult(
                step=step,
                success=False,
                error=f"Tool '{step.tool_name}' not found"
            )
        
        # Try a couple times in case it's a network hiccup
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
                    # Don't retry if it's a client error (like invalid city name)
                    if "not found" in last_error.lower():
                        break
            except Exception as e:
                last_error = str(e)
        
        return StepResult(
            step=step,
            success=False,
            error=last_error or "Execution failed after retries"
        )

