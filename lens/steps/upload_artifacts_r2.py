"""
Upload Artifacts to R2 - Upload transcript and insights JSON to R2 storage
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


def upload_artifacts_r2(job_dir: Path, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upload transcript.json and insights.json to R2 storage

    Args:
        job_dir: Job directory path
        job_data: Job data dict (must contain company info for R2 path)

    Returns:
        Result dict with r2:// URLs for artifacts
    """
    # Get company info for R2 path
    company = job_data.get('company', {})
    confirmed_meta = job_data.get('processing', {}).get('confirm_metadata', {}).get('confirmed', {})

    # Use confirmed metadata if available, else fall back to company data
    ticker = confirmed_meta.get('ticker') or company.get('ticker')
    quarter = confirmed_meta.get('quarter') or company.get('quarter')
    year = confirmed_meta.get('year') or company.get('year')
    job_id = job_data.get('job_id')

    if not all([ticker, quarter, year, job_id]):
        raise ValueError(
            f"Missing required fields for R2 path: ticker={ticker}, quarter={quarter}, year={year}, job_id={job_id}"
        )

    # R2 base path: jobs/{JOB_ID}/artifacts/
    r2_base_path = f"jobs/{job_id}/artifacts"

    artifacts = {}

    # Upload transcript.json
    transcript_file = job_dir / 'transcripts' / 'transcript.json'
    if transcript_file.exists():
        r2_transcript_path = f"{r2_base_path}/transcript.json"
        print(f"📤 Uploading transcript to R2: {r2_transcript_path}")

        cmd = [
            'rclone',
            'copyto',
            str(transcript_file),
            f"r2-markethawkeye:markeyhawkeye/{r2_transcript_path}",
            '--s3-no-check-bucket'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Use r2:// URL format (signed URL generated on-demand)
            transcript_r2_url = f"r2://markeyhawkeye/{r2_transcript_path}"

            # Get file metadata
            file_size = transcript_file.stat().st_size
            with open(transcript_file, 'r') as f:
                transcript_data = json.load(f)
                segment_count = len(transcript_data.get('segments', []))
                speakers = len(set(seg.get('speaker', 'unknown') for seg in transcript_data.get('segments', [])))

            artifacts['transcript'] = {
                'r2_url': transcript_r2_url,
                'r2_path': r2_transcript_path,
                'file_size_bytes': file_size,
                'segment_count': segment_count,
                'speakers': speakers,
                'format': 'whisperx_json',
                'uploaded_at': datetime.now().isoformat()
            }
            print(f"✅ Transcript uploaded: {transcript_r2_url}")
        else:
            print(f"❌ Failed to upload transcript: {result.stderr}")
            raise Exception(f"Transcript upload failed: {result.stderr}")
    else:
        print(f"⚠️  Transcript not found: {transcript_file}")

    # Upload insights.json (check both insights.raw.json and insights.json)
    insights_file = job_dir / 'insights.raw.json'
    if not insights_file.exists():
        insights_file = job_dir / 'insights.json'

    if insights_file.exists():
        r2_insights_path = f"{r2_base_path}/insights.json"
        print(f"📤 Uploading insights to R2: {r2_insights_path}")

        cmd = [
            'rclone',
            'copyto',
            str(insights_file),
            f"r2-markethawkeye:markeyhawkeye/{r2_insights_path}",
            '--s3-no-check-bucket'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            insights_r2_url = f"r2://markeyhawkeye/{r2_insights_path}"

            # Get file metadata
            file_size = insights_file.stat().st_size
            with open(insights_file, 'r') as f:
                insights_data = json.load(f)
                # Extract from nested 'insights' object if present
                insights_obj = insights_data.get('insights', insights_data)
                metrics_count = len(insights_obj.get('financial_metrics', []))
                highlights_count = len(insights_obj.get('highlights', []))

            artifacts['insights'] = {
                'r2_url': insights_r2_url,
                'r2_path': r2_insights_path,
                'file_size_bytes': file_size,
                'metrics_count': metrics_count,
                'highlights_count': highlights_count,
                'format': 'openai_structured_output',
                'uploaded_at': datetime.now().isoformat()
            }
            print(f"✅ Insights uploaded: {insights_r2_url}")
        else:
            print(f"❌ Failed to upload insights: {result.stderr}")
            raise Exception(f"Insights upload failed: {result.stderr}")
    else:
        print(f"⚠️  Insights not found: {insights_file}")

    if not artifacts:
        raise Exception("No artifacts uploaded")

    return {'artifacts': artifacts}
