import pytest
from pipeline.models import IntakeInput
from pipeline.steps import intake_step, extraction_step, classification_step, summarization_step

def test_happy_path_pipeline():
    raw_doc = IntakeInput(document_id="doc_001", raw_text="Invoice Date: 2026-06-15. Total Amount: 1500.00 USD")
    
    intake_out = intake_step(raw_doc)
    extract_out = extraction_step(intake_out)
    classify_out = classification_step(extract_out)
    summary_out = summarization_step(intake_out, classify_out)
    
    assert summary_out.category == "Invoice"
    assert len(extract_out.dates) == 1
    assert "USD" in extract_out.currencies

def test_failure_mode_missing_dates():
    raw_doc = IntakeInput(document_id="doc_002", raw_text="Total Amount: 100.00 USD")
    intake_out = intake_step(raw_doc)
    extract_out = extraction_step(intake_out)
    
    # Assert that our deliberate failure trigger results in missing dates
    assert len(extract_out.dates) == 0

def test_failure_mode_mixed_currencies():
    raw_doc = IntakeInput(document_id="doc_003", raw_text="Date: 2026-06-15. Charge 1: 100 USD. Charge 2: 50 EUR")
    intake_out = intake_step(raw_doc)
    extract_out = extraction_step(intake_out)
    
    # Assert that our deliberate failure trigger captures multiple currencies
    assert "USD" in extract_out.currencies
    assert "EUR" in extract_out.currencies

def test_failure_mode_ambiguous_category():
    # Pass empty extraction data straight to classification to force low confidence
    from pipeline.models import ExtractionOutput
    empty_extract = ExtractionOutput(dates=[], amounts=[], currencies=[])
    classify_out = classification_step(empty_extract)
    
    assert classify_out.category == "Unknown"
    assert classify_out.confidence < 0.50