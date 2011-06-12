"""A typed stack.

Items are pushed onto the stack with a type, with the purpose of being able
to only pop and item of a certain type.
"""

class Stack(object):

    __slots__ = ('_parent', '_item')
    
    def __init__(self, parent=None):
        self._parent = parent
        self._item = None

    def __len__(self):
        i = 0
        this = self
        while this._parent != None:
            i += 1
            this = this._parent
        return i

    def peek(self):
        return self._item

    def pop(self):
        return self._item, self._parent or Stack()

    def push(self, item):
        new_stack = Stack(parent=self)
        new_stack._item = item
        return new_stack

    def reset(self):
        return Stack()

    def __repr__(self):
        return '[%r %r]' % (self._item, self._parent)


class TypedStack(Stack):
    """A stack that stores a type, item on the stack for the purposes of
    restricted popping
    """

    __slots__ = ('_type')

    def __init__(self, parent=None):
        super(TypedStack, self).__init__(parent=parent)
        self._type = None

    def peek(self):
        return (self._type, self._item)

    def pop(self, type=None):
        if self._parent == None:
            raise IndexError("Nothing left on the stack")
        if self._type == type:
            return self._item, self._parent or TypedStack()
        raise ValueError("Couldn't pop value of type '%s'" % type)

    def push(self, *args):
        new_stack = TypedStack(parent=self)
        if len(args) == 2:
            new_stack._type = args[0]
            new_stack._item = args[1]
        else:
            new_stack._type = None
            new_stack._item = args[0]
        return new_stack

    def reset(self):
        return TypedStack()
