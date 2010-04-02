from abstractina.backends import Backend
from abstractina.machines.secd import Cons


class SECDBackend(Backend):

    def compile(self, ast):
        pass

    def dispatch(self, node, accum):
        name = type(node).__name__
        method = getattr(self, 'c_%s' % name)
        if method:
            return method(node, accum)
        raise ValueError("invalid node type found")

    def c_Var(self, node, accum):
        accum.append(('ld', Cons(node.level, node.index),))

    def c_Const(self, node, accum):
        accum.append(('ldc', node.value))

    def c_AddOp(self, node, accum):
        left = self.compile(node.left, accum)
        right = self.compile(node.right, accum)
        accum.append(('add',))

    def c_MultOp(self, node, accum):
        left = self.compile(node.left, accum)
        right = self.compile(node.right, accum)
        accum.append(('mul',))

    def c_SubOp(self, node, accum):
        left = self.compile(node.left, accum)
        right = self.compile(node.right, accum)
        accum.append(('sub',))

    def c_DivOp(self, node, accum):
        left = self.compile(node.left, accum)
        right = self.compile(node.right, accum)
        accum.append(('div',))

    def c_Apply(self, node, accum):
        # compile operands
        accum.append(('nil',))

        # push operands onto the stack
        for operand in node.operands:
            self.compile(operand, accum)
            accum.append(('cons',))

        # push function onto the stack
        # TODO figure this out exactly... how do we know where the function is?
        accum.extend(('ldf', ))
        accum.extend(('ap',))

    def c_Definition(self, node, accum):
        temp_accum = []
        self.compile(node.body)
        # this has to go into the environment, but, how how?
        # TODO
        accum.append(('ret',))

    def c_If(self, node, accum):
        self.compile(node.conditional, accum)
        consequent = []
        alternate = []
        self.compile(node.consequent, consequent)
        consequent.append(('join',))
        self.compile(node.alternate, alternate)
        alternate.append(('join',))
        accum.append(('sel', consequent, alternate))
