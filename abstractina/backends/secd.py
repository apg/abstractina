from abstractina.backends import Backend
from abstractina.data import Cons, List
from abstractina.environment import NameLookupEnvironment, \
    IndexedEnvironment


class SECDBackend(Backend):

    def compile(self, ast, accum=None, env=None):
        return self.dispatch(ast, accum, env or NameLookupEnvironment())

    def dispatch(self, node, accum, env):
        name = type(node).__name__
        method = getattr(self, 'c_%s' % name)
        if method:
            return method(node, accum, env)
        raise ValueError("invalid node type found")

    def c_Var(self, node, accum, env):
        # look up in the environment where node.name is
        level, offset = env[node.name]
        if offset != -1:
            return Cons('ld', 
                        Cons(Cons(level, offset), 
                             accum))
        else:
            raise NameError("'%s' has not been declared" % node.name) 

    def c_Const(self, node, accum, env):
        if node.value is None:
            return Cons('nil', accum)
        return Cons('ldc', Cons(node.value, accum))

    def __compileBinOp(self, operator, node, accum, env):
        t1 = Cons(operator, accum)
        t2 = self.compile(node.right, t1, env)
        return self.compile(node.left, t2, env)

    def c_EqOp(self, node, accum, env):
        return self.__compileBinOp("eq", node, accum, env)

    def c_AddOp(self, node, accum, env):
        return self.__compileBinOp("add", node, accum, env)

    def c_SubOp(self, node, accum, env):
        return self.__compileBinOp("sub", node, accum, env)

    def c_MultOp(self, node, accum, env):
        return self.__compileBinOp("mul", node, accum, env)

    def c_DivOp(self, node, accum, env):
        return self.__compileBinOp("div", node, accum, env)

    def c_Apply(self, node, accum, env):
        t1 = Cons('ap', accum)
        t2 = self.compile(node.function, t1, env)
        localac = Cons("ldf", t2)        

        # push arguments
        for n in node.operands:
            localac = self.compile(n, Cons("cons", localac))

        return Cons(None, localac)

    def c_Lambda(self, node, accum, env):
        t1 = Cons("ret", None)
        # XXX - I'm unsure about this, but think it works.
        return Cons(self.compile(node.body, t1,
                                 env.new_level(node.parameters)),
                        accum)

    def c_Let(self, node, accum, env):
        pass

    def c_LetRec(self, node, accum, env):
        pass

    def c_If(self, node, accum, env):
        t1 = self.compile(node.consequent, List("join"))
        t2 = self.compile(node.alternate, List("join"))
        t3 = Cons("sel", List(t1, t2))
        return self.compile(node.condition, t3)
