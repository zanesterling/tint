class Todo():
    headline = None
    line_number = None
    filepath = None
    text = None

    def __init__(self, headline=None, line=None, filepath=None, text=None):
        self.headline = headline
        self.line_number = line
        self.filepath = filepath
        self.text = text

    # Get and set for mongodb
    def get(self):
        pass

    def put(self):
        pass
