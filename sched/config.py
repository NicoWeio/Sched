from pathlib import Path

import yaml

SCHED_DIR = Path.home() / '.config' / 'sched'
CONFIG_FILE = SCHED_DIR / 'config.yml'
SPOOL_FILE = SCHED_DIR / 'spool.yml'

with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.safe_load(config_file)
