
class Patch():
    raw_patch = []
    old_version = []
    new_version = []

    def __init__(self, patch_text):
        self.raw_patch = patch_text.replace('@@','\nPatch begins\n').split('\n')[2:]
        self.new_version = [line for line in self.raw_patch if line[0] != "-"]
        self.old_version = [line for line in self.raw_patch if line[0] != "+"]

    def addTodo(self):
        pass
