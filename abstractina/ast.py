class AstNode(object):
    pass


class Var(AstNode):

    def __init__(self, level, index, name=None):
        self._level = level
        self._index = index
        self._name = name or 'var-%d-%d' % (level, index)


class Const(AstNode):

    def __init__(self, value):
        self._value = value


class BinOp(AstNode):

    def __init__(self, left, right):
        self._left = left
        self._right = right


class AddOp(BinOp):
    pass


class MultOp(BinOp):
    pass


class Apply(AstNode):

    def __init__(self, function, operands):
        self._function = function
        self._operands = operands


class Definition(AstNode):

    def __init__(self, name, operands, body):
        self._name = name
        self._operands = operands
        self._body = body


class If(AstNode):

    def __init__(self, condition, consequent, alternate):
        self._condition = condition
        self._consequent = consequent
        self._alternate = alternate
