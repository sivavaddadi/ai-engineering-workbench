from pydantic import BaseModel
from typing import List


class RequirementAnalysis(BaseModel):
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    assumptions: List[str]
    open_questions: List[str]
    risks: List[str]
    suggested_apis: List[str]
    test_cases: List[str]