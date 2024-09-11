from flask import Flask, render_template, request, redirect, url_for
import subprocess
from devops_tool import load_deployment_config, deploy_to_environment

app = Flask(__name__)

# Load configurations to display on the UI
config = load_deployment_config()

# Home route to display project and environments
@app.route('/')
def home():
    project = config['deploy']['project']
    environments = config['deploy']['environments']
    return render_template('index.html', project=project, environments=environments)

# Route to trigger deployment for an environment
@app.route('/deploy/<env_name>', methods=['POST'])
def deploy(env_name):
    # Find the environment configuration
    for env in config['deploy']['environments']:
        if env['name'] == env_name:
            deploy_to_environment(
                env_name=env['name'],
                branch=env['branch'],
                pre_checks=env.get('pre-checks', []),
                post_deploy=env.get('post-deploy', []),
                rollback_enabled=env.get('rollback', False)
            )
            break
    return redirect(url_for('home'))

# Route to trigger rollback for an environment
@app.route('/rollback/<env_name>', methods=['POST'])
def rollback(env_name):
    subprocess.run(["git", "reset", "--hard", "HEAD~1"], check=True)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
