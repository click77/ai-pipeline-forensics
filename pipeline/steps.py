from pipeline.models import IntakeInput, IntakeOutput, ExtractionOutput, ClassificationOutput, FinalSummaryOutput

def intake_step(inputs: IntakeInput) -> IntakeOutput:
    """Step 1: Clean and validate raw incoming document text."""
    cleaned = inputs.raw_text.strip()
    return IntakeOutput(document_id=inputs.document_id, cleaned_text=cleaned)
def extraction_step(inputs: IntakeOutput) -> ExtractionOutput:
    """Step 2: Extract key dates, amounts, and currencies. Deliberately fails if data is missing or mixed."""
    text = inputs.cleaned_text.lower()
    
    # Deliberate Failure Mode: Missing Dates
    if "date" not in text:
        return ExtractionOutput(dates=[], amounts=[100.0], currencies=["USD"])
        
    # Deliberate Failure Mode: Mixed Currencies
    if "usd" in text and "eur" in text:
        return ExtractionOutput(dates=["2026-06-15"], amounts=[100.0, 50.0], currencies=["USD", "EUR"])
        
    return ExtractionOutput(dates=["2026-06-15"], amounts=[1500.0], currencies=["USD"])