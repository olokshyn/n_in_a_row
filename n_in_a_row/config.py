from typing import Dict, Any

import yaml


_g_config: Dict[str, Dict[str, Any]] = {}


def load_config(config_filename: str = 'config.yml'):
    global _g_config
    if config_filename in _g_config:
        return _g_config[config_filename]
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)
    _g_config[config_filename] = config
    return config
