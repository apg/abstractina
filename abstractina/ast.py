class AstNode(object):
    pass


class Var(AstNode):

    def __init__(self, level, index, name=None):
        self.level = level
        self.index = index
        self.name = name or 'var-%d-%d' % (level, index)


class Const(AstNode):

    def __init__(self, value):
        self.value = value


class BinOp(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class AddOp(BinOp):
    pass


class SubOp(BinOp):
    pass


class MultOp(BinOp):
    pass


class DivOp(BinOp):
    pass


class Apply(AstNode):

    def __init__(self, function, operands):
        self.function = function
        self.operands = operands


class Definition(AstNode):

    def __init__(self, name, operands, body):
        self.name = name
        self.operands = operands
        self.body = body


class If(AstNode):

    def __init__(self, condition, consequent, alternate):
        self.condition = condition
        self.consequent = consequent
        self.alternate = alternate
