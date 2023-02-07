#!/usr/bin/env python3

import fcntl
import subprocess
from pathlib import Path
from sched import config

import click
import yaml


@click.group()
def cli():
    pass


def fmt_status(job):
    return '\n'.join(f"- {key}: {job[key]}" for key in ['status', 'last_executed', 'last_success'])


@click.command()
@click.argument('job_name', required=False, nargs=-1)
def status(job_name):
    with open(config.SPOOL_FILE, 'r') as spool_file:  # read only – no need to check for lock
        spool_jobs = yaml.safe_load(spool_file)['jobs']

    for job_name in (list(job_name) or spool_jobs.keys()):
        print(f"→ {job_name}")
        print(fmt_status(spool_jobs[job_name]))


@click.command()
@click.option('--only-if-failed', is_flag=True)
@click.argument('job_name', required=False, nargs=-1)
def retry(job_name, only_if_failed=False):
    with open(config.SPOOL_FILE, 'r+') as spool_file:
        try:
            fcntl.flock(spool_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Sched is already running – exiting…')
            exit(2)

        spool = yaml.safe_load(spool_file)

        if not job_name and not only_if_failed:
            click.confirm('Do you really want to re-run ALL jobs?', abort=True)

        for job in (list(job_name) or spool['jobs'].keys()):
            print(f"→ {job}")
            try:
                if not only_if_failed or spool['jobs'][job]['status'] == 'ERROR':
                    spool['jobs'][job]['last_executed'] = None
                    print("Will retry…")
                else:
                    print("Already successful.")
            except KeyError:
                print("Job not found.")

        def update_spool(spool):
            spool_file.seek(0)
            yaml.dump(spool, spool_file, default_flow_style=False)
            spool_file.truncate()
            print("Spool file updated.")

        update_spool(spool)


@click.command()
def run():
    subprocess.run(Path(__file__).resolve().parent / 'main.py')


cli.add_command(status)
cli.add_command(retry)
cli.add_command(run)

if __name__ == '__main__':
    cli()
