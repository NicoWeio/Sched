import yaml

SCHED_DIR = '/home/nicolai/.sched'
CONFIG_FILE = SCHED_DIR + '/config.yml'
SPOOL_FILE = SCHED_DIR + '/spool.yml'

with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.safe_load(config_file)
