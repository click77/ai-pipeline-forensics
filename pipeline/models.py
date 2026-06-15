from pydantic import BaseModel, Field
from typing import List, Optional

# --- Intake Step Models ---
class IntakeInput(BaseModel):
    document_id: str
    raw_text: str

class IntakeOutput(BaseModel):
    document_id: str
    cleaned_text: str

# --- Extraction Step Models ---
class ExtractionOutput(BaseModel):
    dates: List[str] = Field(default_factory=list)
    amounts: List[float] = Field(default_factory=list)
    currencies: List[str] = Field(default_factory=list)

# --- Classification Step Models ---
class ClassificationOutput(BaseModel):
    category: str
    confidence: float

# --- Summarization Step Models ---
class FinalSummaryOutput(BaseModel):
    document_id: str
    category: str
    summary_text: str