import subprocess
import shutil
from datetime import datetime
import yaml

class DeploymentError(Exception):
    """Custom Exception for Deployment Errors."""
    pass

class DSLParser:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_deployment_config(self):
        return self.config.get('deployment', {})

class DevOpsTool:
    def __init__(self, dsl_config_file):
        self.current_branch = 'main'
        self.previous_branch = None
        self.dsl_parser = DSLParser(dsl_config_file)
        self.config = self.dsl_parser.get_deployment_config()

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

        # Pull latest changes
        self.run_git_command(['git', 'pull'])
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

        # Push latest changes
        self.run_git_command(['git', 'push', 'origin', branch, '--force'])

    def rollback(self):
        """Rollback to the previous commit."""
        # Reset to the previous commit
        self.run_git_command(['git', 'reset', '--hard', 'HEAD~1'])

        # Push the changes to the remote repository
        self.run_git_command(['git', 'push', 'origin', self.current_branch, '--force'])

        print(f"Rollback successful. Reset to Previous commit and pushed to remote.")

    def get_deployment_status(self):
        """Return the current deployment status."""
        return f"Currently deployed on branch: {self.current_branch}"

