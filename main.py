#!/usr/bin/env python3

from croniter import croniter
from datetime import datetime, timedelta
import subprocess
import sys
import yaml

SCHED_DIR = '/home/nicolai/.sched'
CONFIG_FILE = SCHED_DIR + '/config.yml'

with open(CONFIG_FILE, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# SPOOL_FILE = f'{config["config"]["spool_dir"]}/spool.yml'
SPOOL_FILE = SCHED_DIR + '/spool.yml'

with open(SPOOL_FILE, 'r') as stream:
    spool = yaml.safe_load(stream)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def notify(msg):
    #TODO: properly escape msg
    process = subprocess.Popen(f'XDG_RUNTIME_DIR=/run/user/$(id -u) /usr/bin/notify-send "{msg}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    o = process.communicate()
    print(o)

class Job:
    def __init__(self, name, data):
        self.name = name
        self.command = data['command']
        self.schedule = data['schedule']
        # when the job was last executed SUCCESSFULLY
        # self.last_executed = (datetime.now() - timedelta(hours=2)).replace(microsecond=0)
        self.last_executed = spool.get(name, {}).get('last_executed', datetime.min)
        self.last_success = spool.get(name, {}).get('last_success', datetime.min)
        # self.status = None # SUCCESS, FAIL, …?
        self.output = ""
    def __repr__(self):
        return f'<job "{self.name}">'
    def execute(self):
        print(f'⚙ Running: {self.command}')
        # process = subprocess.Popen(self.command.split(), stdout=subprocess.PIPE)
        # process = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True)
        # output, error = process.communicate()
        # print(f"{output=}")
        # print(f"{error=}")

        self.last_executed = datetime.now().replace(microsecond=0)
        # errors are caught in main
        for l in execute(self.command):
            print('· ' + l, end="")
            self.output += '\n' + l
        print("✅ Done!")
        self.last_success = datetime.now().replace(microsecond=0)

    def is_due(self):
        # iter = croniter(self.schedule, self.last_executed)
        iter = croniter(self.schedule, self.last_success)
        next = iter.get_next(datetime)
        # last = self.last_executed
        last = self.last_success
        now = datetime.now().replace(microsecond=0)
        print(f"next: {str(next)}")
        print(f"last: {str(last)}")
        print(f"now:  {str(now)} ")
        return next > last and next < now
        # last < next < now

# notify("I'm alive!")

jobs = [Job(name, data) for name, data in config['jobs'].items()]

did_something = False
has_errors = False
for job in jobs:
    print(job)
    if job.is_due():
        did_something = True
        print(f'⏲ {job} is due!')
        try:
            job.execute()
            notify(f'{job.name} ran successfully ✅')
        except subprocess.CalledProcessError as e:
            print(f'Error executing {job}: {e}', file=sys.stderr)
            notify(f'Error executing {job}: {e}')
            with open(f'{SCHED_DIR}/{job.name}_log.txt', 'w') as error_log_file:
                error_log_file.write(job.output)
            has_errors = True

if not did_something:
    # no need to write that file every minute
    exit(0)

with open(SPOOL_FILE, 'w') as yaml_file:
    job_to_last_executed = {job.name: {'last_executed': job.last_executed, 'last_success': job.last_success} for job in jobs}
    yaml.dump(job_to_last_executed, yaml_file, default_flow_style=False)

if has_errors:
    exit(1)
