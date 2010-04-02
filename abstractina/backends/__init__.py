

class Backend(object):
    """Base class for a compiler backend
    """

    def compile(self, ast):
        raise NotImplemented()

    def c_Var(self, node, accum):
        pass

    def c_Const(self, node, accum):
        pass

    def c_AddOp(self, node, accum):
        pass

    def c_MultOp(self, node, accum):
        pass

    def c_Apply(self, node, accum):
        pass

    def c_Definition(self, node, accum):
        pass

    def c_If(self, node, accum):
        pass
