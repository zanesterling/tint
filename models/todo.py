from pymongo import MongoClient

# initialize our database
client = MongoClient()
db = client.tint_data

class Todo():
    repo = None
    headline = None
    line_number = None
    filepath = None
    text = None
    _id = None

    def __repr__(self):
        return '''repo = %(repo)s
            headline = %(head)s
            line_number = %(ln)s
            filepath = %(fp)s
            text = %(text)s
            _id = %(id)s
            ''' % {"repo": self.repo,
                   "head": self.headline,
                   "ln": self.line_number,
                   "fp": self.filepath,
                   "text": self.text,
                   "id": self._id}

    def __init__(self, headline=None,
                 line_number=None,
                 filepath=None,
                 text=None,
                 repo=None,
                 account=None,
                 committed_by=None):
        self.headline = headline
        self.line_number = line_number
        self.filepath = filepath
        self.text = text
        self.repo = repo
        self.committed_by = committed_by
        self.account = acount

    # Get and set for mongodb
    @staticmethod
    def get(line_number, filepath, repo, account, committed_by):
        doc = db.todos.find_one({"filepath": filepath,
                                 "line_number": line_number,
                                 "repo": repo,
                                 "account": account})
        if doc:
            t = Todo(doc['headline'],
                     doc['line_number'],
                     doc['filepath'],
                     doc['text'],
                     doc['repo'],
                     doc['account'],
                     doc['committed_by'])
            t._id = doc['_id']
            return t
        else:
            raise KeyError("No Todo found in the Database with line_number=" + str(line_number) + " and filepath=" + filepath)

    def put(self):
        """ Save this todo to the database in a form that Todo.get() """
        doc = {"filepath": self.filepath,  \
		"line_number": self.line_number,\
		"text": self.text,			  \
                "headline": self.headline,
                "repo":self.repo,
                "account":self.account,
                "committed_by":self.committed_by}
        if not self._id:
            self._id = db.todos.insert(doc)
        else:  # this doc exists already, update it
            db.todos.update({"_id": self._id}, {"$set": doc})

    def remove(self):
        if self._id:
            db.todos.remove(self._id)
            print "Removing entry with id", self._id
