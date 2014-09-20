import requests
import json
import secrets
from patch import Patch


class Commit():
    def __init__(self, user, repo, commit_id):
        self.user = user
        self.repo = repo
        self.commit_id = commit_id

    def process(self):
        fs = self.getFiles(user=self.user,
                           repo=self.repo,
                           commit_id=self.commit_id)
        for f in fs:
            self.processFile(f)

    def getFiles(self, user=None, repo=None, commit_id=None):
        '''Grabs changed files using the github\
            api for this particular user'''

        url = "https://api.github.com/repos/%(user)s/%(repo)s/commits/%(hash)s"\
            "?client_id=%(client_id)s&client_secret=%(client_secret)s"\
            % {"user": user,
                "repo": repo,
                "hash": commit_id,
                "client_id": secrets.client_id,
                "client_secret": secrets.client_secret}
        print url
        request = requests.get(url)
        json_obj = json.loads(request.text)
        return json_obj["files"]

    def processFile(self, github_file):
        patch = Patch(github_file['patch'], filepath=github_file['filename'])
        patch.updateTodos()

commit = Commit(user="shriken",
                repo="tint",
                commit_id="a15d426e38f01c3a1ae2e796530f562ef84dfd72")

commit.process()
