import subprocess
import sys

from time_limit import time_limit, TimeoutException
from job import Job

def notify(msg):
    #TODO: properly escape msg
    process = subprocess.Popen(f'XDG_RUNTIME_DIR=/run/user/$(id -u) /usr/bin/notify-send "{msg}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    o = process.communicate()

def run(spool, config, SCHED_DIR):
    # notify("I'm alive!")

    jobs = [Job(name, data, spool) for name, data in config['jobs'].items()]

    due_jobs = [job for job in jobs if job.is_due()]
    for job in due_jobs:
        print(f'⏲ {job} is due!')
        try:
            with time_limit(job.time_limit):
                job.execute()
            dur = job.last_success - job.last_executed
            notify(f'{job.name} ran successfully in {dur} ✅')
            job.status = 'SUCCESS'
        except subprocess.CalledProcessError as e:
            print(f'Error executing {job}: {e}', file=sys.stderr)
            notify(f'Error executing {job}: {e}')
            with open(f'{SCHED_DIR}/{job.name}_log.txt', 'w') as error_log_file:
                error_log_file.write(job.output)
            job.status = 'ERROR'
            has_errors = True
        except TimeoutException as e:
            print(f'Timeout executing {job}: {e}', file=sys.stderr)
            notify(f'Timeout executing {job}: {e}')
            job.status = 'ERROR'
            has_errors = True

    job_to_last_executed = {job.name: job.to_spool() for job in jobs}

    return {
        'jobs': job_to_last_executed,
        'did_something': len(due_jobs) > 0,
        # We don't want to signal an error if it's not from the current execution.
        # Therefore, only due_jobs are considered.
        'has_errors': any(job.status == 'ERROR' for job in due_jobs),
    }
