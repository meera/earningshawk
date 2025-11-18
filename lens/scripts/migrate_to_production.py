#!/usr/bin/env python3
"""
Migrate job from dev to production

1. Copy R2 artifacts from dev-markethawkeye to markeyhawkeye
2. Insert record into production database with production R2 URLs
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set production mode
os.environ['DEV_MODE'] = 'false'

# Import after setting DEV_MODE
from steps.match_company import match_company
from steps.update_database import update_database


def migrate_r2_artifacts(job_dir: Path, job_data: dict):
    """
    Copy R2 artifacts from dev bucket to production bucket

    Args:
        job_dir: Job directory
        job_data: Job data from job.yaml
    """
    # Get R2 paths from job data
    upload_artifacts = job_data.get('processing', {}).get('upload_artifacts', {})
    upload_media = job_data.get('processing', {}).get('upload_r2', {})

    artifacts = upload_artifacts.get('artifacts', {})

    # Build list of files to copy
    files_to_copy = []

    # Transcript files
    if 'transcript' in artifacts:
        r2_path = artifacts['transcript'].get('r2_path')
        if r2_path:
            files_to_copy.append(r2_path)

    if 'paragraphs' in artifacts:
        r2_path = artifacts['paragraphs'].get('r2_path')
        if r2_path:
            files_to_copy.append(r2_path)

    if 'job' in artifacts:
        r2_path = artifacts['job'].get('r2_path')
        if r2_path:
            files_to_copy.append(r2_path)

    # Insights
    if 'insights' in artifacts:
        r2_path = artifacts['insights'].get('r2_path')
        if r2_path:
            files_to_copy.append(r2_path)

    # Media file
    media_r2_path = upload_media.get('r2_path')
    if media_r2_path:
        files_to_copy.append(media_r2_path)

    print(f"\n📦 Migrating {len(files_to_copy)} files from dev to production R2:")

    for r2_path in files_to_copy:
        src = f"r2-markethawkeye:dev-markethawkeye/{r2_path}"
        dst = f"r2-markethawkeye:markeyhawkeye/{r2_path}"

        print(f"  📤 {r2_path}")

        cmd = ['rclone', 'copyto', src, dst, '--s3-no-check-bucket']
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  ❌ Failed: {result.stderr}")
            raise Exception(f"R2 copy failed: {result.stderr}")

        print(f"  ✅ Copied")

    print(f"\n✅ All R2 artifacts migrated to production\n")


def migrate_database(job_dir: Path, job_data: dict):
    """
    Insert record into production database

    Args:
        job_dir: Job directory
        job_data: Job data from job.yaml
    """
    print("🔄 Migrating database record to production...")

    # First match company to get CIK
    print("\n🔍 Matching company...")
    match_result = match_company(job_dir, job_data)

    # Add match result to job_data
    if 'processing' not in job_data:
        job_data['processing'] = {}
    job_data['processing']['match_company'] = match_result

    # Update database with production R2 URLs
    print("\n💾 Inserting into production database...")
    db_result = update_database(job_dir, job_data)

    print(f"\n✅ Database migration complete!")

    return db_result


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Migrate job from dev to production')
    parser.add_argument('job_yaml', help='Path to job.yaml file')
    parser.add_argument('--r2-only', action='store_true', help='Only migrate R2 artifacts')
    parser.add_argument('--db-only', action='store_true', help='Only migrate database')
    parser.add_argument('--skip-r2', action='store_true', help='Skip R2 migration')

    args = parser.parse_args()

    job_file = Path(args.job_yaml)
    if not job_file.exists():
        print(f"❌ Job file not found: {job_file}")
        sys.exit(1)

    job_dir = job_file.parent

    # Load job data
    with open(job_file, 'r') as f:
        job_data = yaml.safe_load(f)

    job_id = job_data.get('job_id')
    print(f"\n🚀 Migrating job: {job_id}")
    print(f"   From: dev-markethawkeye (dev DB)")
    print(f"   To: markeyhawkeye (production DB)")
    print()

    # Confirm
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("❌ Cancelled")
        sys.exit(0)

    # Migrate R2
    if not args.db_only and not args.skip_r2:
        migrate_r2_artifacts(job_dir, job_data)

    # Migrate database
    if not args.r2_only:
        migrate_database(job_dir, job_data)

    print(f"\n🎉 Migration complete!")
    print(f"\n📊 Production record ID: {job_data.get('job_id')}")


if __name__ == '__main__':
    main()
