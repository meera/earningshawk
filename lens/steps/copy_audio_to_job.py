"""
Copy Audio to Job - Copy manually downloaded audio file to job directory
"""

import shutil
from pathlib import Path
from typing import Dict, Any


def copy_audio_to_job(job_dir: Path, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Copy audio file from source path to job input directory

    Args:
        job_dir: Job directory path
        job_data: Job data dict (must contain 'audio_source' with path to audio file)

    Returns:
        Result dict with status and output path
    """
    # Get source audio path from job data
    audio_source = job_data.get('audio_source')
    if not audio_source:
        raise ValueError("job_data must contain 'audio_source' field with path to audio file")

    source_path = Path(audio_source)
    if not source_path.exists():
        raise FileNotFoundError(f"Audio file not found: {source_path}")

    # Create input directory if needed
    input_dir = job_dir / "input"
    input_dir.mkdir(parents=True, exist_ok=True, mode=0o755)

    # Determine output filename (preserve extension)
    output_filename = f"source{source_path.suffix}"  # e.g., source.mp3, source.wav
    output_path = input_dir / output_filename

    # Copy file
    print(f"📁 Copying audio file...")
    print(f"   From: {source_path}")
    print(f"   To: {output_path}")

    shutil.copy2(source_path, output_path)

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✅ Audio file copied ({file_size_mb:.1f} MB)")

    return {
        'source': str(source_path),
        'destination': str(output_path),
        'file_size_mb': round(file_size_mb, 2),
    }
