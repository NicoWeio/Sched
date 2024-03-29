import subprocess
from datetime import datetime, timedelta

from croniter import croniter


def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    for stdout_line in iter(p.stdout.readline, ""):
        yield stdout_line
    p.stdout.close()
    return_code = p.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


class Job:
    def __init__(self, name, data, spool):
        self.name = name
        self.command = data['command']
        self.schedule = data['schedule']
        self.time_limit = data.get('time_limit', 60*15)  # TODO: configurable default
        # when the job was STARTED
        self.last_executed = spool['jobs'].get(name, {}).get('last_executed', datetime.min)
        # when the job ended SUCCESSFULLY
        self.last_success = spool['jobs'].get(name, {}).get('last_success', datetime.min)
        self.status = spool['jobs'].get(name, {}).get('status')
        self.output = ""

    def __repr__(self):
        return f'<job "{self.name}">'

    def to_spool(self):
        return {
            'last_executed': self.last_executed,
            'last_success': self.last_success,
            'status': self.status,
        }

    def execute(self):
        print(f'⚙ Running: {self.command}')
        self.last_executed = datetime.now().replace(microsecond=0)
        # errors are caught in main
        for l in run_cmd(self.command):
            print('· ' + l, end="")
            self.output += '\n' + l.strip()
        print("✅ Done!")
        self.last_success = datetime.now().replace(microsecond=0)

    def is_due(self):
        if self.status == None or self.status == 'SUCCESS':
            return self.is_due_regular()
        if self.status == 'DISABLED':
            print(f'{self} is disabled!')
            return False
        if self.status == 'ERROR':
            last = self.last_executed
            now = datetime.now().replace(microsecond=0)
            next = last + timedelta(hours=1)  # TODO don't hardcode
            return next < now

    def is_due_regular(self):
        last = self.last_success
        iter = croniter(self.schedule, last)
        next = iter.get_next(datetime)  # >last
        now = datetime.now().replace(microsecond=0)
        print(f"next: {str(next)}")
        print(f"last: {str(last)}")
        print(f"now:  {str(now)} ")
        return next < now
        # last < next < now
