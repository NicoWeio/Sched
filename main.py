#!/usr/bin/env python3

import fcntl
from runner import run
import yaml

SCHED_DIR = '/home/nicolai/.sched'
CONFIG_FILE = SCHED_DIR + '/config.yml'
SPOOL_FILE = SCHED_DIR + '/spool.yml'

with open(SPOOL_FILE, 'r+') as spool_file:
    try:
        fcntl.flock(spool_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as e:
        print('Sched is already running – exiting…')
        exit(-1)

    spool = yaml.safe_load(spool_file)
    with open(CONFIG_FILE, 'r') as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)

    run_result = run(spool, config, SCHED_DIR)

    print(run_result)

    if not run_result['did_something']:
        # no need to write that file every minute
        exit(0)
    else:
        spool_file.seek(0)
        yaml.dump({'jobs': run_result['jobs']}, spool_file, default_flow_style=False)
        spool_file.truncate()

    if run_result['has_errors']:
        exit(1)
