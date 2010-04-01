

class Backend(object):
    """Base class for a compiler backend
    """

    def compile(self, ast):
        raise NotImplemented()
