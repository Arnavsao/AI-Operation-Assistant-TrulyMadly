"""
Verifier Agent - Validates results and ensures output quality
"""
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from llm.client import LLMClient
from agents.planner import ExecutionPlan
from agents.executor import StepResult


class VerificationResult(BaseModel):
    """Result of verification"""
    is_complete: bool = Field(description="Whether all required data was obtained")
    is_valid: bool = Field(description="Whether the data is valid and useful")
    missing_data: List[str] = Field(description="List of missing or incomplete data points")
    quality_score: int = Field(description="Quality score from 1-10")
    suggestions: List[str] = Field(description="Suggestions for improvement")


class FinalOutput(BaseModel):
    """Final structured output"""
    task_summary: str = Field(description="Summary of the completed task")
    status: str = Field(description="Overall status: success, partial, or failed")
    results: Dict[str, Any] = Field(description="Structured results from all steps")
    metadata: Dict[str, Any] = Field(description="Metadata about execution")


class VerifierAgent:
    """
    Verifier Agent - Validates execution results and formats final output
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def verify_and_format(
        self,
        plan: ExecutionPlan,
        step_results: List[StepResult]
    ) -> FinalOutput:
        """
        Verify results and create final output
        
        Args:
            plan: Original execution plan
            step_results: Results from executor
            
        Returns:
            Final formatted output
        """
        # Check completion status
        successful_steps = [r for r in step_results if r.success]
        failed_steps = [r for r in step_results if not r.success]
        
        # Determine overall status
        if len(failed_steps) == 0:
            status = "success"
        elif len(successful_steps) > 0:
            status = "partial"
        else:
            status = "failed"
        
        # Verify quality using LLM
        verification = self._verify_quality(plan, step_results)
        
        # Format results
        results = self._format_results(step_results)
        
        # Create metadata
        metadata = {
            "total_steps": len(step_results),
            "successful_steps": len(successful_steps),
            "failed_steps": len(failed_steps),
            "quality_score": verification.quality_score,
            "verification": {
                "is_complete": verification.is_complete,
                "is_valid": verification.is_valid,
                "missing_data": verification.missing_data,
                "suggestions": verification.suggestions
            }
        }
        
        # Add error details if any
        if failed_steps:
            metadata["errors"] = [
                {
                    "step": r.step.step_number,
                    "tool": r.step.tool_name,
                    "error": r.error
                }
                for r in failed_steps
            ]
        
        return FinalOutput(
            task_summary=plan.task_summary,
            status=status,
            results=results,
            metadata=metadata
        )
    
    def _verify_quality(
        self,
        plan: ExecutionPlan,
        step_results: List[StepResult]
    ) -> VerificationResult:
        """Use LLM to verify result quality"""
        system_prompt = """You are a Verifier Agent in an AI Operations Assistant system.

Your role is to validate execution results and assess their quality.

Evaluate:
1. Completeness - Did we get all expected data?
2. Validity - Is the data useful and relevant?
3. Quality - How well does it answer the user's task?

Provide constructive feedback and suggestions."""
        
        # Prepare results summary for LLM
        results_summary = []
        for result in step_results:
            results_summary.append({
                "step": result.step.description,
                "success": result.success,
                "has_data": result.data is not None,
                "error": result.error
            })
        
        user_prompt = f"""Task: {plan.task_summary}
Expected Output: {plan.expected_output}

Execution Results:
{results_summary}

Verify the quality and completeness of these results."""
        
        try:
            verification_data = self.llm.generate_structured_output(
                prompt=user_prompt,
                system_prompt=system_prompt,
                response_format=VerificationResult,
                temperature=0.3
            )
            return VerificationResult(**verification_data)
        except Exception:
            # Fallback verification
            successful = sum(1 for r in step_results if r.success)
            total = len(step_results)
            
            return VerificationResult(
                is_complete=successful == total,
                is_valid=successful > 0,
                missing_data=[r.step.description for r in step_results if not r.success],
                quality_score=int((successful / total) * 10) if total > 0 else 0,
                suggestions=["Some steps failed - check error details"]
            )
    
    def _format_results(self, step_results: List[StepResult]) -> Dict[str, Any]:
        """Format step results into structured output"""
        formatted = {}
        
        for result in step_results:
            tool_name = result.step.tool_name
            
            if result.success and result.data:
                # Group results by tool type
                if tool_name not in formatted:
                    formatted[tool_name] = []
                formatted[tool_name].append(result.data)
            
        return formatted
