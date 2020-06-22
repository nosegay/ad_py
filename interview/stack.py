class StackElement:
    def __init__(self, predecessor, value):
        self.predecessor = predecessor
        self.value = value


class Stack:
    def __init__(self, value):
        self.stack_top = StackElement(None, value)

    def isEmpty(self):
        return self.stack_top.predecessor is None

    def push(self, value):
        self.stack_top = StackElement(self.stack_top, value)

    def pop(self):
        top = self.stack_top.value
        self.stack_top = self.stack_top.predecessor
        return top

    def peek(self):
        return self.stack_top.value

    def size(self):
        length = 0
        element = self.stack_top
        while element.predecessor is not None:
            length += 1
            element = element.predecessor

        return length


