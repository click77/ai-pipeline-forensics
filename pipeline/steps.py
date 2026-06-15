from pipeline.models import IntakeInput, IntakeOutput, ExtractionOutput, ClassificationOutput, FinalSummaryOutput

def intake_step(inputs: IntakeInput) -> IntakeOutput:
    """Step 1: Clean and validate raw incoming document text."""
    cleaned = inputs.raw_text.strip()
    return IntakeOutput(document_id=inputs.document_id, cleaned_text=cleaned)