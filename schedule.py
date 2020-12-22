from jira import JIRA


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


if __name__ == "__main__":
    email = 'nguyenvanthu1905@gmail.com'
    apiToken = 'rk02aXQlAqLKw8y6jhEl43E'
    server = 'https://issuse.atlassian.net'
    fields = {
        'project': {'id': 10000},
        'summary': 'Good morning everybody.',
        'issuetype': {
            'name': 'Emailed request'
        }
    }
    connection = connect(email, apiToken, server)
    if connection['error']:
        print(connection['error'])
    else:
        task = create_task(connection['connection'], fields)
        if task:
            print(task)
