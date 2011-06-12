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
        return Cons('ld', 
                    Cons(Cons(node.level, node.index), 
                         accum))

    def c_Const(self, node, accum):
        if node.value is None:
            return Cons('nil', accum)
        return Cons('ldc', Cons(node.value, accum))

    def __compileBinOp(self, operator, node, accum):
        t1 = Cons(operator, accum)
        t2 = self.compile(node.right, t1)
        return self.compile(node.left, t2)

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
        t1 = Cons('ap', accum)
        t2 = self.compile(node.function, t1)
        localac = Cons("ldf", t2)        

        # push arguments
        for n in node.operands:
            localac = self.compile(n, Cons("cons", localac))

        return Cons(None, localac)

    def c_Lambda(self, node, accum):
        t1 = Cons("ret", None)
        return Cons(self.compile(node.body, t1), accum)

    def c_If(self, node, accum):
        """CD SEL (CN JOIN) (AL JOIN)"""
        t1 = self.compile(node.consequent, List("join"))
        t2 = self.compile(node.alternate, List("join"))
        t3 = Cons("sel", List(t1, t2))
        return self.compile(node.condition, t3)
