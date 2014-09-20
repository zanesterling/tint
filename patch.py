from models.todo import Todo


class Patch():
    raw_patch = []
    old_version = []
    new_version = []
    filepath = ""
    new_version_line_start = None
    old_version_line_start = None

    def __init__(self, patch_text, filepath):
        self.raw_patch = patch_text.replace('@@', '\nPatch begins\n').\
            split('\n')[2:]
        self.new_version = [line for line in self.raw_patch if line[0] != "-"]
        self.old_version = [line for line in self.raw_patch if line[0] != "+"]
        self.old_version_line_start = int(self.raw_patch[0].replace("-", "").\
            split(",")[0].strip(" "))
        self.new_version_line_start = int(self.raw_patch[0].replace("+", ",").\
            split(",")[2])
        self.file_path = filepath

    def updateTodos(self):
        new_todos = self.findNewTodos()
        deleted_todos = self.findDeletedTodos()
        coupled_todos = self.findCoupledTodos()
        for key in new_todos:
            new_todos[key].put()

    def findCoupledTodos(self):
        old_search = {}
        new_search = {}
        coupled_dict = {}
        old_idx = self.old_version_line_start
        new_idx = self.new_version_line_start
        for line in self.new_version:
            line = line.lower()
            if line[0]!="+" and self.containsTodo(line):
                index = line.find("todo")
                todo_text = line[index:]
                new_todo = Todo(headline=todo_text,
                                line_number=new_idx,
                                filepath=self.file_path,
                                text=todo_text
                                )
                new_search[new_idx] = new_todo
            new_idx += 1

        for line in self.old_version:
            line = line.lower()
            if line[0]!="-" and self.containsTodo(line):
                index = line.find("todo")
                todo_text = line[index:]
                old_todo = Todo(headline=todo_text,
                                line_number=old_idx,
                                filepath=self.file_path,
                                text=todo_text
                                )
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
            line = line.lower()
            if line[0]=="+" and self.containsTodo(line):
                index = line.find("todo")
                todo_text = line[index:]
                new_todo = Todo(headline=todo_text,
                                line_number=idx,
                                filepath=self.file_path,
                                text=todo_text
                                )
                new_todo_dict[idx] = new_todo
            idx += 1
        return new_todo_dict

    def findDeletedTodos(self):
        idx = self.old_version_line_start - 2
        deleted_todo_dict = {}
        for line in self.old_version:
            line = line.lower()
            if line[0]=="-" and self.containsTodo(line):
                index = line.find("todo")
                todo_text = line[index:]
                deleted_todo = Todo(headline=todo_text,
                                line_number=idx,
                                filepath=self.file_path,
                                text=todo_text
                                )
                deleted_todo_dict[idx] = deleted_todo
            idx+=1
        return deleted_todo_dict

    def containsTodo(self, line):
        if "todo" in line:
            return True
