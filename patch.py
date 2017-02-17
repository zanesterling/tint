from models.todo import Todo


class Patch():
    patch_lines = []
    old_version = []
    new_version = []
    filepath = ""
    new_version_start_line = None
    old_version_start_line = None
    repo = None
    account = None
    committed_by = None

    def __init__(self, patch_text, filepath, repo, account, committed_by):
        self.account = account
        self.committed_by = committed_by
        self.file_path = filepath
        self.repo = repo

        lines = patch_text.split('\n')
        header_line = lines[0]
        self.patch_lines = [l if len(l) > 0 else " " for l in lines[1:]]

        # Convert from '@@ -1,2 +3,4 @@ ...' to [1,2,3,4].
        header = header_line.split('@@')[1].strip(' -').replace('+', ',').split(',')
        self.old_version_start_line = int(header[0])
        self.new_version_start_line = int(header[2])

        self.new_version = [l for l in self.patch_lines if l[0] != "-"]
        self.old_version = [l for l in self.patch_lines if l[0] != "+"]

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
        for i, line in enumerate(self.new_version):
            if line[0] != "+" and containsTodo(line):
                index = findTodo(line)
                todo_text = line[index:]
                line_num = self.new_version_start_line + i

                new_todo = Todo(headline     = todo_text,
                                committed_by = self.committed_by,
                                account      = self.account,
                                line_number  = line_num,
                                filepath     = self.file_path,
                                text         = todo_text,
                                repo         = self.repo)
                new_search[line_num] = new_todo

        for i, line in enumerate(self.old_version):
            if line[0] != "-" and containsTodo(line):
                index = findTodo(line)
                todo_text = line[index:]
                line_num = self.old_version_start_line + i

                new_todo = Todo(headline     = todo_text,
                                committed_by = self.committed_by,
                                account      = self.account,
                                line_number  = line_num,
                                filepath     = self.file_path,
                                text         = todo_text,
                                repo         = self.repo)
                old_search[line_num] = old_todo

        for old_key in old_search:
            for new_key in new_search:
                if old_search[old_key].headline == new_search[new_key].headline:
                    coupled_dict[(old_key, new_key)] = (old_search[old_key], new_search[new_key])

        return coupled_dict

    def findNewTodos(self):
        new_todos = {}
        for i, line in enumerate(self.new_version):
            if line[0]=="+" and containsTodo(line):
                index = findTodo(line)
                todo_text = line[index:]
                line_num = self.new_version_start_line + i

                new_todo = Todo(headline     = todo_text,
                                committed_by = self.committed_by,
                                account      = self.account,
                                line_number  = line_num,
                                filepath     = self.file_path,
                                text         = todo_text,
                                repo         = self.repo)
                new_todos[line_num] = new_todo

        return new_todos

    def findDeletedTodos(self):
        deleted_todos = {}
        for i, line in enumerate(self.new_version):
            if line[0]=="-" and containsTodo(line):
                index = findTodo(line)
                todo_text = line[index:]
                line_num = self.old_version_start_line + i

                new_todo = Todo(headline     = todo_text,
                                committed_by = self.committed_by,
                                account      = self.account,
                                line_number  = line_num,
                                filepath     = self.file_path,
                                text         = todo_text,
                                repo         = self.repo)
                new_todos[line_num] = new_todo

        return deleted_todos

def containsTodo(line):
    return bool(findTodo(line))

def findTodo(line):
    stripped = line[1:].lstrip()
    commentseq = None
    possibleseqs = ['#', '//'] # possible (one-line) comment starters
    for seq in possibleseqs:
        if stripped.startswith(seq):
            commentseq = seq
    if commentseq:
        # slice off the comment, strip whitespace again, and check for TODO at the beginning
        sliced = stripped[len(commentseq):].lstrip()
        if sliced.startswith('TODO'):
            return (len(line) - len(sliced))
    return None;


def test_parser():
    pass

if __name__ == '__main__':
    test_parser()
