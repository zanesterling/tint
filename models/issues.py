
class Issue():
    title = None #Required. The title of the issue.
    body = None #The contents of the issue.
    assignee = None #Login for the user that this issue should be assigned to.
    labels = None #Labels to associate with this issue.

    def __init__(self, title=None, body=None, assignee=None, labels=None):
        self.title = title
        self.body = body
        self.assignee = assignee
        self.labels = labels

    #Get and set for mongodb
    def get():
        pass

    def set():
        pass

