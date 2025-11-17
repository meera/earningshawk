"""
Workflow Orchestrator - Execute composable workflows defined in YAML

Replaces hardcoded pipeline logic with flexible workflow execution
"""

import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Add lens to path
LENS_DIR = Path(__file__).parent
PROJECT_ROOT = LENS_DIR.parent
sys.path.insert(0, str(LENS_DIR))
sys.path.insert(0, str(LENS_DIR / "scripts"))

from job import JobManager
from step_registry import get_handler, list_handlers


class WorkflowOrchestrator:
    """Execute workflow steps defined in YAML"""

    def __init__(self, job_file: Path, workflow_file: Optional[Path] = None, force: bool = False):
        """
        Initialize workflow orchestrator

        Args:
            job_file: Path to job.yaml
            workflow_file: Optional path to custom workflow YAML (overrides job's workflow)
            force: Force re-run completed steps
        """
        self.job = JobManager(job_file)
        self.job_dir = job_file.parent
        self.workflow = self._load_workflow(workflow_file)
        self.force = force

    def _load_workflow(self, workflow_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load workflow definition from YAML

        Args:
            workflow_file: Optional custom workflow file (overrides job.yaml workflow)

        Returns:
            Workflow dict with 'name', 'description', 'steps'
        """
        if workflow_file:
            # Custom workflow file provided
            with open(workflow_file, 'r') as f:
                workflow = yaml.safe_load(f)
            print(f"📋 Loaded custom workflow: {workflow['name']}")
            return workflow

        # Load workflow from job.yaml
        workflow_name = self.job.job.get('workflow')
        if not workflow_name:
            raise ValueError(
                "No workflow specified. Job must have 'workflow' field or provide --workflow-file"
            )

        # Load workflow template from lens/workflows/
        workflow_path = LENS_DIR / "workflows" / f"{workflow_name}.yaml"
        if not workflow_path.exists():
            raise FileNotFoundError(
                f"Workflow template not found: {workflow_path}\n"
                f"Available workflows: {list((LENS_DIR / 'workflows').glob('*.yaml'))}"
            )

        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)

        print(f"📋 Loaded workflow: {workflow['name']} - {workflow.get('description', '')}")
        return workflow

    def _evaluate_condition(self, condition: str) -> bool:
        """
        Evaluate skip condition (Python expression)

        Args:
            condition: Python expression (e.g., "processing.transcribe.status != 'completed'")

        Returns:
            True if condition is met (should skip), False otherwise
        """
        # Create evaluation context with job data
        context = {
            'job': self.job.job,
            'processing': self.job.job.get('processing', {}),
            'company': self.job.job.get('company', {}),
            'insights': self.job.job.get('processing', {}).get('extract_insights', {}).get('data', {}),
            'metadata': self.job.job.get('metadata', {}),
        }

        try:
            # Evaluate condition safely
            result = eval(condition, {"__builtins__": {}}, context)
            return bool(result)
        except Exception as e:
            print(f"⚠️  Warning: Failed to evaluate condition '{condition}': {e}")
            return False  # Don't skip on evaluation error

    def _should_skip_step(self, step: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Check if step should be skipped

        Args:
            step: Step definition from workflow

        Returns:
            (should_skip, reason) tuple
        """
        step_name = step['name']
        processing = self.job.job.get('processing', {})

        # Check if step already completed (unless --force flag is used)
        if not self.force and step_name in processing:
            step_status = processing[step_name].get('status')
            if step_status == 'completed':
                return (True, f"already completed")

        # Check skip_if condition
        skip_if = step.get('skip_if')
        if skip_if:
            if self._evaluate_condition(skip_if):
                return (True, f"condition met: {skip_if}")

        return (False, None)

    def _execute_step(self, step: Dict[str, Any]) -> bool:
        """
        Execute single workflow step

        Args:
            step: Step definition from workflow

        Returns:
            True if step succeeded, False if failed
        """
        step_name = step['name']
        handler_name = step['handler']
        required = step.get('required', True)
        description = step.get('description', '')

        print(f"\n{'='*60}")
        print(f"Step: {step_name}")
        print(f"Handler: {handler_name}")
        if description:
            print(f"Description: {description}")
        print(f"{'='*60}\n")

        # Check if should skip
        should_skip, skip_reason = self._should_skip_step(step)
        if should_skip:
            print(f"⏭️  Skipping {step_name}: {skip_reason}")
            return True

        # Mark step as in progress
        self.job.update_step(step_name, status='in_progress', started_at=datetime.now().isoformat())

        try:
            # Get handler function
            handler = get_handler(handler_name)

            # Execute handler
            # Handlers receive (job_dir, job_data) and return result dict
            result = handler(self.job_dir, self.job.job)

            # Update job with result (merge result dict into step data)
            self.job.update_step(
                step_name,
                status='completed',
                completed_at=datetime.now().isoformat(),
                **result
            )

            print(f"✅ {step_name} completed")
            return True

        except Exception as e:
            error_msg = f"Failed: {str(e)}"
            self.job.update_step(
                step_name,
                status='failed',
                error=error_msg,
                failed_at=datetime.now().isoformat()
            )

            print(f"❌ {step_name} failed: {e}")

            if required:
                print(f"\n⚠️  Step '{step_name}' is required. Stopping workflow.")
                raise
            else:
                print(f"\n⚠️  Step '{step_name}' is optional. Continuing workflow.")
                return False

    def run_all(self):
        """Execute all steps in workflow"""
        print(f"\n{'#'*60}")
        print(f"# Workflow: {self.workflow['name']}")
        print(f"# Job: {self.job.job['job_id']}")
        print(f"# Total Steps: {len(self.workflow['steps'])}")
        print(f"{'#'*60}\n")

        self.job.set_status("processing")

        successful_steps = 0
        failed_steps = 0
        skipped_steps = 0

        for step in self.workflow['steps']:
            try:
                success = self._execute_step(step)
                if success:
                    successful_steps += 1
                else:
                    failed_steps += 1
            except Exception:
                failed_steps += 1
                break  # Stop on required step failure

        total_steps = len(self.workflow['steps'])
        print(f"\n{'#'*60}")
        print(f"# Workflow Summary")
        print(f"{'#'*60}")
        print(f"Total: {total_steps}")
        print(f"✅ Successful: {successful_steps}")
        print(f"❌ Failed: {failed_steps}")
        print(f"⏭️  Skipped: {total_steps - successful_steps - failed_steps}")
        print(f"{'#'*60}\n")

        if failed_steps == 0:
            self.job.set_status("completed")
            print("🎉 Workflow completed successfully!")
        else:
            self.job.set_status("failed")
            print("⚠️  Workflow incomplete. See errors above.")

    def run_step(self, step_name: str):
        """
        Execute single step by name

        Args:
            step_name: Name of step to execute
        """
        # Find step in workflow
        step = next((s for s in self.workflow['steps'] if s['name'] == step_name), None)

        if not step:
            available = [s['name'] for s in self.workflow['steps']]
            raise ValueError(
                f"Step '{step_name}' not found in workflow '{self.workflow['name']}'\n"
                f"Available steps: {', '.join(available)}"
            )

        print(f"\n{'#'*60}")
        print(f"# Running Single Step: {step_name}")
        print(f"# Workflow: {self.workflow['name']}")
        print(f"# Job: {self.job.job['job_id']}")
        print(f"{'#'*60}\n")

        self._execute_step(step)

    def run_from_step(self, start_step_name: str):
        """
        Execute workflow starting from specific step

        Args:
            start_step_name: Name of step to start from
        """
        # Find step index
        step_names = [s['name'] for s in self.workflow['steps']]
        if start_step_name not in step_names:
            raise ValueError(
                f"Step '{start_step_name}' not found in workflow\n"
                f"Available steps: {', '.join(step_names)}"
            )

        start_index = step_names.index(start_step_name)

        print(f"\n{'#'*60}")
        print(f"# Workflow: {self.workflow['name']}")
        print(f"# Starting from: {start_step_name}")
        print(f"# Steps to execute: {len(self.workflow['steps']) - start_index}")
        print(f"{'#'*60}\n")

        # Execute from start_index onwards
        for step in self.workflow['steps'][start_index:]:
            try:
                self._execute_step(step)
            except Exception:
                print(f"\n⚠️  Stopping workflow at {step['name']}")
                break


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Execute MarketHawk workflows")
    parser.add_argument("job_file", type=Path, help="Path to job.yaml")
    parser.add_argument(
        "--workflow-file",
        type=Path,
        help="Custom workflow YAML (overrides job.yaml workflow)"
    )
    parser.add_argument("--step", help="Run single step only")
    parser.add_argument("--from-step", help="Run from specific step onwards")
    parser.add_argument("--force", action="store_true", help="Force re-run completed steps")
    parser.add_argument("--list-handlers", action="store_true", help="List available step handlers")

    args = parser.parse_args()

    # List handlers mode
    if args.list_handlers:
        print("\n📦 Registered Step Handlers:\n")
        handlers = list_handlers()
        for name, status in sorted(handlers.items()):
            icon = "✅" if status == "available" else "⚠️"
            print(f"{icon} {name:40} {status}")
        print()
        return

    # Validate job file
    if not args.job_file.exists():
        print(f"❌ Job file not found: {args.job_file}")
        sys.exit(1)

    # Create orchestrator
    orchestrator = WorkflowOrchestrator(args.job_file, args.workflow_file, force=args.force)

    # Execute workflow
    if args.step:
        orchestrator.run_step(args.step)
    elif args.from_step:
        orchestrator.run_from_step(args.from_step)
    else:
        orchestrator.run_all()


if __name__ == "__main__":
    main()
