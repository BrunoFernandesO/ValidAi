from typing import List, Optional
from pydantic import BaseModel

class ValidationError(BaseModel):
    code: str
    message: str

class ValidationCheck(BaseModel):
    name: str
    value: Optional[str] = None
    status: str # ok | error
    errors: Optional[List[ValidationError]] = None

class ValidationResult(BaseModel):
    filename: str
    approved: bool
    stage: str
    summary: str
    file_url: str
    checks: List[ValidationCheck]

class ValidationResponse(BaseModel):
    results: List[ValidationResult]