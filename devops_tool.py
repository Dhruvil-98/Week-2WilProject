import subprocess
import shutil
from datetime import datetime

class DeploymentError(Exception):
    """Custom Exception for Deployment Errors."""
    pass

class DevOpsTool:
    def __init__(self):
        self.current_branch = 'main'
        self.previous_branch = None

    def run_git_command(self, command, check=True):
        """Helper function to run Git commands."""
        try:
            result = subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise DeploymentError(f"Git command failed: {e.stderr.strip()}")

    def pre_deployment_checks(self):
        """Perform pre-deployment checks like code review status and required environment variables."""
        # Example check for uncommitted changes
        status = self.run_git_command(['git', 'status', '--porcelain'], check=False)
        if status:
            self.auto_commit_changes()

        # Add other checks like environment variables if needed
        # required_env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
        # for var in required_env_vars:
        #     if not shutil.which(var):
        #         raise DeploymentError(f"Missing required environment variable: {var}")

    def auto_commit_changes(self):
        """Automatically commit uncommitted changes with a unique commit message."""
        print("Uncommitted changes detected. Automatically committing changes...")

        # Stage all changes
        self.run_git_command(['git', 'add', '.'])

        # Generate a unique commit message
        commit_message = f"Auto-commit before deployment on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Commit the changes
        self.run_git_command(['git', 'commit', '-m', commit_message])

        print(f"Changes committed with message: {commit_message}")

    def deploy(self, branch):
        """Deploy the specified branch."""
        self.pre_deployment_checks()

        # Stash changes if necessary
        self.run_git_command(['git', 'stash'])

        # Fetch latest changes
        self.run_git_command(['git', 'fetch'])

        # Checkout branch
        self.previous_branch = self.current_branch
        self.run_git_command(['git', 'checkout', branch])
        self.current_branch = branch

        # Pull latest changes
        self.run_git_command(['git', 'pull'])
        # Push latest changes
        self.run_git_command(['git', 'push', 'origin', branch, '--force'])
    def rollback(self):
        """Rollback to the previous branch."""
        if not self.previous_branch:
            raise DeploymentError("No previous branch to roll back to.")

        self.run_git_command(['git', 'checkout', self.previous_branch])
        self.current_branch = self.previous_branch
        self.previous_branch = None

    def get_deployment_status(self):
        """Return the current deployment status."""
        return f"Currently deployed on branch: {self.current_branch}"

