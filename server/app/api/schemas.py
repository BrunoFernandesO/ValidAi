from typing import List, Optional
from pydantic import BaseModel

class ValidationError(BaseModel):
    code: str
    message: List[str]

class ValidationCheck(BaseModel):
    name: str
    value: Optional[str] = None
    status: str # ok | error
    errors: Optional[List[ValidationError]] = None

class ValidationResult(BaseModel):
    filename: str
    approved: bool
    summary: str
    file_url: str
    checks: List[ValidationCheck]

class ValidationResponse(BaseModel):
    total: int
    approved: int
    failed: int
    results: List[ValidationResult]