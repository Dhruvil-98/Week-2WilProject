import yaml
import subprocess
import os

# Utility function to read YAML-based DSL configuration
def load_deployment_config(config_file='deploy.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Pre-deployment checks such as running tests or checking approvals
def run_pre_deployment_checks(checks):
    for check in checks:
        if check == "run-tests":
            result = run_tests()
        elif check == "approval-required":
            result = request_approval()
        if not result:
            print(f"Pre-deployment check {check} failed.")
            return False
    return True

# Simulated test runner
def run_tests():
    print("Running tests...")
    # Simulate running tests
    return True

# Simulated manual approval
def request_approval():
    print("Requesting manual approval...")
    # Simulate approval (auto-approve for the sake of simplicity)
    return True

# Rollback mechanism for failed deployments
def rollback_deployment():
    print("Rolling back to previous version...")
    try:
        # Reverting the last commit (Git)
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], check=True)
        print("Rollback successful.")
    except subprocess.CalledProcessError:
        print("Rollback failed!")

# Deployment function
def deploy_to_environment(env_name, branch, pre_checks, post_deploy=None, rollback_enabled=False):
    print(f"\nDeploying to {env_name} (Branch: {branch})...")

    # Checkout the branch
    subprocess.run(["git", "checkout", branch], check=True)

    # Run pre-deployment checks
    if not run_pre_deployment_checks(pre_checks):
        print(f"Pre-deployment checks failed for {env_name}. Aborting deployment.")
        if rollback_enabled:
            rollback_deployment()
        return

    # Simulate deployment process
    print(f"Deploying {env_name}...")
    subprocess.run(["echo", "Deploying..."], check=True)

    # Run post-deployment actions
    if post_deploy:
        for action in post_deploy:
            if action == "notify-team":
                notify_team()

    print(f"Deployment to {env_name} completed successfully.\n")

# Simulated post-deployment notification
def notify_team():
    print("Notifying the team...")

# Main function to handle deployment based on DSL configuration
def main():
    # Load deployment configuration from DSL
    config = load_deployment_config()

    project = config['deploy']['project']
    environments = config['deploy']['environments']

    print(f"Starting deployment for project: {project}")

    # Loop through each environment
    for env in environments:
        deploy_to_environment(
            env_name=env['name'],
            branch=env['branch'],
            pre_checks=env.get('pre-checks', []),
            post_deploy=env.get('post-deploy', []),
            rollback_enabled=env.get('rollback', False)
        )

if __name__ == "__main__":
    main()
