from models.todo import Todo


class Patch():
    raw_patch = []
    old_version = []
    new_version = []
    filepath = ""
    new_version_line_start = None
    old_version_line_start = None
    repo = None
    account = None
    committed_by = None

    def __init__(self, patch_text, filepath, repo, account, committed_by):
        self.raw_patch = patch_text.replace("@@\n", "\nPatch begins\n")
        self.raw_patch = self.raw_patch.replace('@@', '\nPatch begins\n').\
            split('\n')[2:]

        self.account = account
        self.committed_by = committed_by

        idx = 0
        for line in self.raw_patch:
            if len(line)==0:
                line = " "
                self.raw_patch[idx] = line
            idx+=1

        self.new_version = [l for l in self.raw_patch if line[0] != "-"]
        self.old_version = [l for l in self.raw_patch if line[0] != "+"]
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
                todo = Todo.get(line_number=ln, filepath=fp,
                                repo=self.repo, account=self.account,
                                committed_by=self.committed_by)
                todo.remove()
            except KeyError, e:
                print e.message
                print "This todo was already deleted"

        for key in new_todos:
            ln = new_todos[key].line_number
            fp = new_todos[key].filepath
            try:
                Todo.get(line_number=ln, filepath=fp,
                         repo=self.repo, account=self.account,
                         committed_by=self.committed_by)
                print "Todo already exists"
            except KeyError:
                new_todos[key].put()

        for key in coupled_todos:
            if True:
                ln = key[0]
                fp = coupled_todos[key][0].filepath
                try:
                    todo = Todo.get(line_number=ln, filepath=fp, repo=self.repo, account=self.account, committed_by=self.committed_by)
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
                index = self.findTodo(line)
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
                index = self.findTodo(line)
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
                index = self.findTodo(line)
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
                index = self.findTodo(line)
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
        return bool(self.findTodo(line))

    def findTodo(self, line):
        stripped = line.lstrip()
        commentseq = None
        possibleseqs = ['#', '//'] # possible (one-line) comment starters
        for seq in possibleseqs:
            if stripped.startswith(seq):
                commentseq = seq
        if commentseq:
            # slice off the comment, strip whitespace again, and check for TODO at the beginning
            sliced = stripped[len(commentseq)].lstrip()
            if sliced.startswith('TODO:'):
                return len(line) - len(sliced)
        return None;

