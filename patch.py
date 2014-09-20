from models.todo import Todo


class Patch():
    raw_patch = []
    old_version = []
    new_version = []
    filepath = ""
    new_version_line_start = None
    old_version_line_start = None
    repo = None

    def __init__(self, patch_text, filepath, repo):
        self.raw_patch = patch_text.replace("@@\n", "\nPatch begins\n")
        self.raw_patch = self.raw_patch.replace('@@', '\nPatch begins\n').\
            split('\n')[2:]

        idx = 0
        for line in self.raw_patch:
            if len(line)==0:
                line = " "
                self.raw_patch[idx] = line
            idx+=1

        self.new_version = [line for line in self.raw_patch if line[0] != "-"]
        self.old_version = [line for line in self.raw_patch if line[0] != "+"]
        self.old_version_line_start = int(self.raw_patch[0].replace("-", "").\
            split(",")[0].strip(" "))
        self.new_version_line_start = int(self.raw_patch[0].replace("+", ",").\
            split(",")[2])
        self.file_path = filepath
        self.repo = repo

    def updateTodos(self):
        new_todos = self.findNewTodos()
        deleted_todos = self.findDeletedTodos()
        coupled_todos = self.findCoupledTodos()

        print new_todos
        print deleted_todos
        print coupled_todos


        for key in deleted_todos:
            ln = deleted_todos[key].line_number
            fp = deleted_todos[key].filepath
            try:
                todo = Todo.get(line_number=ln, filepath=fp, repo=self.repo)
                todo.remove()
            except KeyError, e:
                print e.message
                print "This todo was already deleted"

        for key in new_todos:
            ln = new_todos[key].line_number
            fp = new_todos[key].filepath
            try:
                Todo.get(line_number=ln, filepath=fp, repo=self.repo)
                print "Todo already exists"
            except KeyError:
                new_todos[key].put()

        for key in coupled_todos:
            if True:
                ln = key[0]
                fp = coupled_todos[key][0].filepath
                try:
                    todo = Todo.get(line_number=ln, filepath=fp, repo=self.repo)
                    todo.line_number = key[1]
                    todo.filepath = coupled_todos[key][1].filepath
                    todo.put()
                except KeyError:
                    print "No such todo found. Making one now."
                    coupled_todos[key][1].put()


    def findCoupledTodos(self):
        old_search = {}
        new_search = {}
        coupled_dict = {}
        #subtract 2 from line numbers because patch starts with patch metadata
        old_idx = self.old_version_line_start - 2
        new_idx = self.new_version_line_start - 2
        for line in self.new_version:
            if line[0]!="+" and self.containsTodo(line):
                index = line.find("TODO")
                todo_text = line[index:]
                new_todo = Todo(headline=todo_text,
                                line_number=new_idx,
                                filepath=self.file_path,
                                text=todo_text,
                                repo=self.repo)
                new_search[new_idx] = new_todo
            new_idx += 1

        for line in self.old_version:
            if line[0]!="-" and self.containsTodo(line):
                index = line.find("TODO")
                todo_text = line[index:]
                old_todo = Todo(headline=todo_text,
                                line_number=old_idx,
                                filepath=self.file_path,
                                text=todo_text,
                                repo=self.repo)
                old_search[old_idx] = old_todo
            old_idx += 1

        for old_key in old_search:
            for new_key in new_search:
                if old_search[old_key].headline == new_search[new_key].headline:
                    coupled_dict[(old_key, new_key)] = \
                        (old_search[old_key], new_search[new_key])

        return coupled_dict

    def findNewTodos(self):
        idx = self.new_version_line_start - 2
        new_todo_dict = {}
        for line in self.new_version:
            if line[0]=="+" and self.containsTodo(line):
                index = line.find("TODO")
                todo_text = line[index:]
                new_todo = Todo(headline=todo_text,
                                line_number=idx,
                                filepath=self.file_path,
                                text=todo_text,
                                repo=self.repo)
                new_todo_dict[idx] = new_todo
            idx += 1
        return new_todo_dict

    def findDeletedTodos(self):
        idx = self.old_version_line_start - 2
        deleted_todo_dict = {}
        for line in self.old_version:
            if line[0]=="-" and self.containsTodo(line):
                index = line.find("TODO")
                todo_text = line[index:]
                deleted_todo = Todo(headline=todo_text,
                                line_number=idx,
                                filepath=self.file_path,
                                text=todo_text,
                                repo=self.repo
                                    )
                deleted_todo_dict[idx] = deleted_todo
            idx+=1
        return deleted_todo_dict

    def containsTodo(self, line):
        if "#TODO" in line:
            return True
