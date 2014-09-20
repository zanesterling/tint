import requests
import json
import secrets


def commit_processor(user, repo, commit_id):
    files = getFiles(user=user, repo=repo, commit_id=commit_id)
    for f in files:
        processFile(f)


def getFiles(user=None, repo=None, commit_id=None):
    url = "https://api.github.com/repos/%(user)s/%(repo)s/commits/%(hash)s"\
        "?client_id=%(client_id)s&client_secret=%(client_secret)s"\
        % {"user": user,
           "repo": repo,
           "hash": commit_id,
           "client_id": secrets.client_id,
           "client_secret": secrets.client_secret}

    request = requests.get(url)
    json_obj = json.loads(request.text)
    return json_obj["files"]


def processFile(github_file):
    print github_file['patch']

commit_processor(user="Prinzhorn",
                 repo="skrollr",
                 commit_id="5bf8668b413232f49d19387a3931f0b421971efe")
