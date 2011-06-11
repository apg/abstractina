class AstNode(object):
    pass


class Var(AstNode):

    def __init__(self, level, index, name=None):
        self.level = level
        self.index = index
        self.name = name or 'var-%d-%d' % (level, index)

    def __repr__(self):
        return '<Var name=%s, level=%d, index=%d>' % (name, level, index)


class Const(AstNode):

    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return '<Const: value=%s>' % self.value


class BinOp(AstNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '<%s: left=%s, right=%s>' % \
            (type(self).__name__, repr(self.left), repr(self.right))


class AddOp(BinOp):
    pass


class SubOp(BinOp):
    pass


class MultOp(BinOp):
    pass


class DivOp(BinOp):
    pass


class EqOp(BinOp):
    pass


class Apply(AstNode):

    def __init__(self, function, operands):
        self.function = function
        self.operands = operands


class Lambda(AstNode):
    
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body


class If(AstNode):

    def __init__(self, condition, consequent, alternate):
        self.condition = condition
        self.consequent = consequent
        self.alternate = alternate
