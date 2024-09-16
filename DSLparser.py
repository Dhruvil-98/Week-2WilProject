import yaml

class DSLParser:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_deployment_config(self):
        return self.config.get('deployment', {})
