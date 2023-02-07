#!/usr/bin/env python3

import fcntl
from sched.config import SPOOL_FILE
from sched.runner import run

import yaml


def main():
    # notify('Test', body='Is this thing on?', icon='dialog-question', urgency='LOW')
    with open(SPOOL_FILE, 'r+') as spool_file:
        try:
            fcntl.flock(spool_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as e:
            print('Sched is already running – exiting…')
            return 2

        spool = yaml.safe_load(spool_file)

        run_result = run(spool)

        print(run_result)

        if not run_result['did_something']:
            # no need to write that file every minute
            return 0
        else:
            spool_file.seek(0)
            yaml.dump({'jobs': run_result['jobs']}, spool_file, default_flow_style=False)
            spool_file.truncate()

        if run_result['has_errors']:
            return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
