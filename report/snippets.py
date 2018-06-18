def hello_world():
    return "Hello world"


class Counter(object):
    def __init__(self):
        self.val = 0

    def add(self):
        self.val += 1
        return self.val
