from typing import Dict, Any, Tuple

import yaml


_g_config: Dict[str, Dict[str, Any]] = {}


def load_config(config_filename: str = 'config.yml') -> Dict[str, Any]:
    global _g_config
    if config_filename in _g_config:
        return _g_config[config_filename]
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)
    _g_config[config_filename] = config
    return config


def max_grid_shape() -> Tuple[int, int]:
    config = load_config()
    return config['max_grid_rows'], config['max_grid_cols']
