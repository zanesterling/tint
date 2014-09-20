from pymongo import MongoClient

# initialize our database
client = MongoClient()
db = client.tint_data

class Todo():
	headline = None
	line_number = None
	filepath = None
	text = None
	obj_id = None

	def __init__(self, headline=None, line=None, filepath=None, text=None):
		self.headline = headline
		self.line_number = line
		self.filepath = filepath
		self.text = text

	# Get and set for mongodb
	@staticmethod
	def get(line_number, filepath):
		doc = db.todos.find_one({"filepath": filepath, "line_number": line_number})
	t = Todo(doc['headline'], doc['line_number'], doc['filepath'], doc['text'])
	t._id = doc['_id'];
	return t

	def put(self):
		""" Save this todo to the database in a form that Todo.get() """
		doc = { "filepath": self.filepath,  \
			"line_number": self.line_number,\
			"text": self.text,			  \
			"headline": self.headline}		   
	if not self._id:
		self._id = db.todos.insert(doc)
	else: # this doc exists already, update it
		db.todos.update({"_id": self._id}, {"$set": doc})
