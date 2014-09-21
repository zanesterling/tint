import requests
import json
import db

class Issue():
    title = None #Required. The title of the issue.
    body = None #The contents of the issue.
    assignee = None #Login for the user that this issue should be assigned to.
    labels = None #Labels to associate with this issue.
    access_token = None

    def __init__(self, title=None, body=None, assignee=None, labels=None):
        self.title = title
        self.body = body
        self.assignee = assignee
        self.labels = labels
        self.access_token = db.getToken("tintapplication")

    # Get and set for mongodb
    def get():
        pass


    def set(self, account, repo):
        url = '''https://api.github.com/repos/%(act)s/%(repo)s/issues?%(token)s'''\
            %{"token":self.access_token,
              "act": account,
              "repo": repo}
        payload = {'title': self.title,
                   'body': self.body,
                   'assignee': self.assignee,
                   'labels': self.labels}
        response = requests.post(url, data=json.dumps(payload))
        number = json.loads(response.text)['number']
        return number

    @staticmethod
    def remove(issue_number, account, repo):
        url = '''https://api.github.com/repos/%(act)s/%(repo)s/issues?%(token)s'''\
            %{"token":self.access_token,
              "act": account,
              "repo": repo}
        payload = {'state':'closed'}
        response = requests.post(url, data=json.dumps(payload))
