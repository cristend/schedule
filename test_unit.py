import unittest
import os
from os.path import join, dirname
from dotenv import load_dotenv
from schedule import connect, create_task, main
from cronjob import CronJob
from crontab import CronTab


class TestSchedule(unittest.TestCase):
    connection = connect(
        'nguyenvanthu1905@gmail.com',
        'rk02aXQlAqLKw8y6jhEl43E0',
        'https://issuse.atlassian.net'
    )

    def test_connect_success(self):
        email = 'nguyenvanthu1905@gmail.com'
        apiToken = 'rk02aXQlAqLKw8y6jhEl43E0'
        server = 'https://issuse.atlassian.net'
        self.assertTrue(connect(email, apiToken, server)['connection'])

    def test_connect_incorrect_server(self):
        email = 'nguyenvanthu1905@gmail.com'
        apiToken = 'rk02aXQlAqLKw8y6jhEl43E0'
        server = 'https://issuses.atlassian.net'
        self.assertFalse(connect(email, apiToken, server)['connection'])

    def test_connect_incorrect_token(self):
        email = 'nguyenvanthu1905@gmail.com'
        apiToken = 'rk02aXQlAqLKw8y6jhEl43E'
        server = 'https://issuse.atlassian.net'
        self.assertFalse(connect(email, apiToken, server)['connection'])

    def test_connect_incorrect_email(self):
        email = 'nguyenvanthu19@gmail.com'
        apiToken = 'rk02aXQlAqLKw8y6jhEl43E0'
        server = 'https://issuse.atlassian.net'
        self.assertEqual(connect(email, apiToken, server)
                         ['error'], 'email incorrect')

    def test_create_task_success(self, connection=connection['connection']):
        fields = {
            'project': {'id': 10000},
            'summary': 'Good morning everybody.',
            'issuetype': {
                'name': 'Emailed request'
            }
        }
        self.assertTrue(create_task(connection, fields)['task'])

    def test_create_task_fail(self, connection=connection['connection']):
        fields_1 = {
            'project': {'id': 2000},
            'summary': 'Good morning everybody.',
            'issuetype': {
                'name': 'Emailed request'
            }
        }
        fields_2 = {
            'project': {'id': 2000},
            'summary': 'Good morning everybody.',
            'issuetype': {
                'name': 'Emailed request'
            }
        }
        fields_3 = {
            'project': {'id': 2000},
            'summary': 'Good morning everybody.',
        }
        fields_4 = {
            'project': {'id': 2000},
            'summary': 'Good morning everybody.',
            'issuetype': {
                'name': 'Thing that not exist'
            }
        }
        self.assertFalse(create_task(connection, fields_1)['task'])
        self.assertFalse(create_task(connection, fields_2)['task'])
        self.assertFalse(create_task(connection, fields_3)['task'])
        self.assertFalse(create_task(connection, fields_4)['task'])

    def test_main(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        email = os.environ.get('EMAIL')
        token = os.environ.get('APITOKEN')
        server = os.environ.get('SERVER')
        self.assertTrue(main(email, token, server).get('task'))


class TestCronJob(unittest.TestCase):
    def test_init(self):
        self.assertTrue(isinstance(CronJob().cron, CronTab))

    def test_create(self):
        cron = CronJob()
        current_cron = len(cron.cron)
        cron.create('ls')
        cron_assert = CronJob()
        self.assertEqual(len(cron_assert.cron), current_cron+1)

    def test_remove(self):
        cron = CronJob()
        cron.remove()
        cron_assert = CronJob()
        self.assertEqual(len(cron_assert.cron), 0)

    def test_command(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        virtual_path = os.environ.get('VIRTUAL_PATH')
        filename = os.environ.get('FILENAME')
        path = os.path.join(os.getcwd(), filename)
        command = virtual_path + path
        test = os.system(command)
        self.assertEqual(test, 0)
