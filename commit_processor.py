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
        committed_by = fs["commit"]["author"]["name"]
        for f in fs["files"]:
            self.processFile(f, committed_by)

    def getFiles(self, user=None, repo=None, commit_id=None):
        '''Grabs changed files using the github\
            api for this particular user'''

        url = "https://api.github.com/repos/%(user)s/%(repo)s/commits/%(hash)s"\
            "?client_id=%(client_id)s&client_secret=%(client_secret)s"\
            % {"user": user,
                "repo": repo,
                "hash": commit_id,
                "client_id": secrets.CLIENT_ID,
                "client_secret": secrets.CLIENT_SECRET}
        print url
        request = requests.get(url)
        json_obj = json.loads(request.text)
        return json_obj

    def processFile(self, github_file, committed_by):
        patch = Patch(patch_text=github_file['patch'],
                      filepath=github_file['filename'],
                      repo=self.repo,
                      account=self.user,
                      committed_by=committed_by)
        patch.updateTodos()


if __name__=="__main__":
    commit = Commit(user="shriken",
                    repo="tint",
                    commit_id="c170680d71607b09d33069ab8b0c8dd22989d60c")

    commit.process()
