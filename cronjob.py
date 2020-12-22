import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
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
        self.cron.write()


if __name__ == "__main__":
    args = sys.argv
    flag = None
    if len(args) > 1:
        flag = args[1]
    if flag == 'clear':
        CronJob().remove()
    else:
        filename = os.environ.get('FILENAME')
        path = os.path.join(os.getcwd(), filename)
        virtual_path = os.environ.get('VIRTUAL_PATH')
        command = virtual_path + path
        job = CronJob().create(command)
