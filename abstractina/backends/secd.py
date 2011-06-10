from abstractina.backends import Backend
from abstractina.data import Cons, List


class SECDBackend(Backend):

    def compile(self, ast, accum=None):
        return self.dispatch(ast, accum)

    def dispatch(self, node, accum):
        name = type(node).__name__
        method = getattr(self, 'c_%s' % name)
        if method:
            return method(node, accum)
        raise ValueError("invalid node type found")

    def c_Var(self, node, accum):
        return Cons(List('ld', Cons(node.level, node.index),), accum)

    def c_Const(self, node, accum):
        return Cons(List('ldc', node.value), accum)

    def __compileBinOp(self, operator, node, accum):
        right = self.compile(node.right, accum)
        print right
        left = self.compile(node.left, accum)
        print left
        return Cons(right, 
                    Cons(left, 
                         Cons(Cons(operator, None), accum)))

    def c_EqOp(self, node, accum):
        return self.__compileBinOp("eq", node, accum)

    def c_AddOp(self, node, accum):
        return self.__compileBinOp("add", node, accum)

    def c_SubOp(self, node, accum):
        return self.__compileBinOp("sub", node, accum)

    def c_MultOp(self, node, accum):
        return self.__compileBinOp("mul", node, accum)

    def c_DivOp(self, node, accum):
        return self.__compileBinOp("div", node, accum)

    def c_Apply(self, node, accum):
        pass

    def c_Definition(self, node, accum):
        pass

    def c_If(self, node, accum):
        conditional = self.compile(node.conditional, accum)
        consequent = self.compile(node.consequent, accum)
        alternate = []
        self.compile(node.consequent, consequent)
        consequent.append(('join',))
        self.compile(node.alternate, alternate)
        alternate.append(('join',))
        accum.append(('sel', consequent, alternate))
