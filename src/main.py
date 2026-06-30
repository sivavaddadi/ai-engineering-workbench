from fastapi import FastAPI
from pydantic import BaseModel
from services.llm_service import analyze_requirement
from models.response_models import RequirementAnalysis


app = FastAPI(title="AI Engineering Workbench")


class AnalyzeRequest(BaseModel):
    requirement: str


@app.post("/analyze", response_model=RequirementAnalysis)
def analyze(request: AnalyzeRequest) -> RequirementAnalysis:
    """
    Analyze a business requirement using AI.
    
    Args:
        request: Request body containing the requirement text
        
    Returns:
        RequirementAnalysis: Structured analysis of the requirement
    """
    return analyze_requirement(request.requirement)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
