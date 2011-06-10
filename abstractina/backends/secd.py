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
        return List('ld', Cons(node.level, node.index),)

    def c_Const(self, node, accum):
        return List('ldc', node.value)

    def __compileBinOp(self, operator, node, accum):
        right = self.compile(node.right)
        left = self.compile(node.left)
        return List(right, left, Cons(operator, None))

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
        """XXX: I guess this has to be a let/letrec.. """
        pass

    def c_If(self, node, accum):
        condition = self.compile(node.condition)
        consequent = self.compile(node.consequent)
        alternate = self.compile(node.alternate)

        return List(condition,
                    List(List('sel'),
                         List(consequent, List('join')),
                         List(alternate, List('join'))))






