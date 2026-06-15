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
def classification_step(inputs: ExtractionOutput) -> ClassificationOutput:
    """Step 3: Classify document type based on extractions. Deliberately drops confidence if ambiguous."""
    # Deliberate Failure Mode: Ambiguous Category (No explicit financial attributes)
    if not inputs.amounts:
        return ClassificationOutput(category="Unknown", confidence=0.30)
        
    return ClassificationOutput(category="Invoice", confidence=0.95)
def summarization_step(intake: IntakeOutput, classification: ClassificationOutput) -> FinalSummaryOutput:
    """Step 4: Compile the final processing summary output."""
    summary_text = f"Document processed as {classification.category} with {classification.confidence * 100}% confidence."
    return FinalSummaryOutput(
        document_id=intake.document_id,
        category=classification.category,
        summary_text=summary_text
    )