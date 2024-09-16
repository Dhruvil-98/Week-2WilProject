from flask import Flask, render_template, request, redirect, url_for, flash
from devops_tool import DevOpsTool, DeploymentError
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
devops = DevOpsTool('deploy.yaml')  # Load DSL configuration file


# Home page route
@app.route('/')
def home():
    status = devops.get_deployment_status()
    return render_template('index.html', status=status)

# Route to trigger deployment
@app.route('/deploy', methods=['POST'])
def deploy():
    try:
        branch = request.form.get('branch')
        if not branch:
            flash('Please select a branch for deployment.')
            return redirect(url_for('home'))

        # Trigger deployment
        devops.deploy(branch)
        flash(f'Successfully deployed branch {branch}!', 'success')

    except DeploymentError as e:
        flash(f'Deployment failed: {str(e)}', 'danger')

    return redirect(url_for('home'))

# Route to handle rollback
@app.route('/rollback', methods=['POST'])
def rollback():
    try:
        devops.rollback()
        flash('Rollback was successful!', 'success')

    except DeploymentError as e:
        flash(f'Rollback failed: {str(e)}', 'danger')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
