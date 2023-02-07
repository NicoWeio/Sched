import subprocess
import sys

from .config import SCHED_DIR, config
from .job import Job
from .notifications import notify
from .time_limit import TimeoutException, time_limit


def run(spool):
    # notify("I'm alive!")

    jobs = [Job(name, data, spool) for name, data in config['jobs'].items()]

    due_jobs = [job for job in jobs if job.is_due()]
    for job in due_jobs:
        print(f'⏲ {job} is due!')
        try:
            with time_limit(job.time_limit):
                job.execute()
            dur = job.last_success - job.last_executed
            notify(job.name, f'ran successfully in {dur}', icon='dialog-positive')
            job.status = 'SUCCESS'
        except subprocess.CalledProcessError as e:
            print(f'Error executing {job}: {e}', file=sys.stderr)
            notify(job.name, f'encountered an error: {e}', icon='dialog-error', urgency='CRITICAL')
            with open(f'{SCHED_DIR}/{job.name}_log.txt', 'w') as error_log_file:
                error_log_file.write(job.output)
            job.status = 'ERROR'
            has_errors = True
        except TimeoutException as e:
            print(f'Timeout executing {job}: {e}', file=sys.stderr)
            notify(job.name, 'timed out', icon='dialog-error', urgency='CRITICAL')
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
