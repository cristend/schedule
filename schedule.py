from jira import JIRA
import os
from os.path import join, dirname
from dotenv import load_dotenv


def connect(email, apiToken, server):
    try:
        connection = JIRA(server, basic_auth=(email, apiToken))
    except Exception as error:
        return {
            'error': error,
            'connection': None
        }
    if not connection.projects():
        return {
            'error': 'email incorrect',
            'connection': None
        }
    return {
        'error': None,
        'connection': connection
    }


def create_task(connection, fields):
    try:
        task = connection.create_issue(fields=fields)
    except Exception as error:
        return {
            'error': error,
            'task': None
        }
    return {'error': None, 'task': task}


def main(email=None, apiToken=None, server=None, fields=None):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    email = os.environ.get('EMAIL') if not email else email
    apiToken = os.environ.get('APITOKEN') if not apiToken else apiToken
    server = os.environ.get('SERVER') if not server else server
    fields = ({
        'project': {'id': 10000},
        'summary': 'Good morning everybody.',
        'issuetype': {'name': 'Emailed request'}
    }if not fields else fields)

    connection = connect(email, apiToken, server)
    if connection['error']:
        return connection
    else:
        task = create_task(connection['connection'], fields)
        return task


if __name__ == "__main__":
    main()
