from pathlib import Path

import yaml

from .config_defaults import EXAMPLE_CONFIG, EXAMPLE_SPOOL

SCHED_DIR = Path.home() / '.config' / 'sched'
CONFIG_FILE = SCHED_DIR / 'config.yml'
SPOOL_FILE = SCHED_DIR / 'spool.yml'

try:
    config = yaml.safe_load(CONFIG_FILE.read_text())
except FileNotFoundError:
    # create config file
    SCHED_DIR.mkdir(parents=False, exist_ok=True)
    CONFIG_FILE.write_text(yaml.dump(EXAMPLE_CONFIG, default_flow_style=False))
    print(f"Created example config file at {CONFIG_FILE}")

    # also create an empty spool file
    if not SPOOL_FILE.exists():
        SPOOL_FILE.write_text(yaml.dump(EXAMPLE_SPOOL, default_flow_style=False))
        print(f"Created example spool file at {SPOOL_FILE}")

    # set the example config so we can continue
    config = EXAMPLE_CONFIG
