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
        patch = Patch(patch_text=github_file['patch'],
                      filepath=github_file['filename'],
                      repo=self.repo)
        patch.updateTodos()

commit = Commit(user="shriken",
                repo="tint",
                commit_id="53cfdced8ac6a9c2f3b3085a18a381092e30e8a6")

commit.process()
