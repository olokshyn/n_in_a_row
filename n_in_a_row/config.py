import yaml


def load_config(config_filename: str = 'config.yml'):
    with open(config_filename) as config_file:
        return yaml.safe_load(config_file)
