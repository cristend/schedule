import os
from crontab import CronTab


class CronJob():
    def __init__(self):
        self.cron = CronTab(user=True)

    def create(self, command):
        job = self.cron.new(command=command)
        job.hour.on(9)
        job.minute.on(0)
        self.cron.write()

    def remove(self):
        self.cron.remove_all()


if __name__ == "__main__":
    filename = 'schedule.py'
    path = os.path.join(os.getcwd(), filename)
    virtual_path = '/home/cristend/.local/share/virtualenvs/Bai1-E4ZZKRKx/bin/python3 '
    command = virtual_path + path
    job = CronJob().create(command)
