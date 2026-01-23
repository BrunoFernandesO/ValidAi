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
    approved: bool
    summary: str
    checks: List[ValidationCheck]