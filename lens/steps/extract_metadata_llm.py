"""
Extract Metadata from Transcript using LLM

Analyzes transcript to extract ticker, company name, quarter, and year
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel


class EarningsMetadata(BaseModel):
    """Structured output for earnings call metadata"""
    ticker: Optional[str] = None
    company: Optional[str] = None
    quarter: Optional[str] = None  # e.g., "Q3", "Q4"
    year: Optional[int] = None
    confidence: str = "low"  # low, medium, high


def extract_metadata_llm(job_dir: Path, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract metadata from transcript using OpenAI

    Args:
        job_dir: Job directory path
        job_data: Job data dict

    Returns:
        Result dict with extracted metadata
    """
    # Load transcript
    transcript_path = job_dir / "transcripts" / "transcript.json"
    if not transcript_path.exists():
        raise FileNotFoundError(
            f"Transcript not found: {transcript_path}\n"
            "Run 'transcribe' step first"
        )

    with open(transcript_path, 'r') as f:
        transcript_data = json.load(f)

    # Extract text from transcript (first 10 minutes for metadata extraction)
    # Usually ticker/company/quarter announced in first few minutes
    segments = transcript_data.get('segments', [])
    text_segments = []
    for seg in segments:
        if seg['start'] > 600:  # 10 minutes
            break
        text_segments.append(seg['text'])

    transcript_text = ' '.join(text_segments)

    if not transcript_text.strip():
        raise ValueError("Transcript is empty - cannot extract metadata")

    print(f"🤖 Extracting metadata from transcript using OpenAI...")
    print(f"   Analyzing first 10 minutes ({len(transcript_text)} chars)")

    # Call OpenAI with structured output
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": """You are an expert at analyzing earnings call transcripts.
Extract the following metadata from the transcript:

1. ticker: Stock symbol (e.g., "NVDA", "AAPL", "GOOGL")
2. company: Full legal company name (e.g., "NVIDIA Corporation", "Apple Inc.")
3. quarter: Fiscal quarter (e.g., "Q1", "Q2", "Q3", "Q4")
4. year: Fiscal year (e.g., 2024, 2025)

Look for clues in:
- Opening remarks (e.g., "Welcome to Apple's Q3 2024 earnings call")
- Speaker introductions (e.g., "I'm Tim Cook, CEO of Apple")
- Financial statements (e.g., "For the third quarter of fiscal 2024...")

If you cannot find a value with confidence, leave it null.
Set confidence to 'high' if you found explicit mentions, 'medium' if inferred, 'low' if guessing."""
            },
            {
                "role": "user",
                "content": f"Extract metadata from this earnings call transcript:\n\n{transcript_text}"
            }
        ],
        response_format=EarningsMetadata,
    )

    metadata = completion.choices[0].message.parsed

    print(f"\n📊 Extracted Metadata:")
    print(f"   Ticker: {metadata.ticker or '(not found)'}")
    print(f"   Company: {metadata.company or '(not found)'}")
    print(f"   Quarter: {metadata.quarter or '(not found)'}")
    print(f"   Year: {metadata.year or '(not found)'}")
    print(f"   Confidence: {metadata.confidence}")
    print()

    return {
        'extracted': {
            'ticker': metadata.ticker,
            'company': metadata.company,
            'quarter': metadata.quarter,
            'year': metadata.year,
        },
        'confidence': metadata.confidence,
        'method': 'llm',
        'model': 'gpt-4o-2024-08-06',
    }
