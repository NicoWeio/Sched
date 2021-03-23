import subprocess
import sys

from job import Job

def notify(msg):
    #TODO: properly escape msg
    process = subprocess.Popen(f'XDG_RUNTIME_DIR=/run/user/$(id -u) /usr/bin/notify-send "{msg}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    o = process.communicate()

def run(spool, config, SCHED_DIR):
    notify("I'm alive!")

    jobs = [Job(name, data, spool) for name, data in config['jobs'].items()]

    did_something = False
    has_errors = False
    for job in jobs:
        print(job)
        if job.is_due():
            did_something = True
            print(f'⏲ {job} is due!')
            try:
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

    job_to_last_executed = {job.name: job.to_spool() for job in jobs}

    return {
        'jobs': job_to_last_executed,
        'did_something': did_something,
        'has_errors': has_errors,
    }
