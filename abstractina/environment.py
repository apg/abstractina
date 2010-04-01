"""A common environment that uses De Bruijin indices instead of names
"""

class Environment(object):

    __slots__ = ('_level', '_parent',)

    def __init__(self, values=None, parent=None):
        self._parent = parent
        self._level = values or []

    def new_level(self, values=None):
        new_env = Environment(values=values, parent=self)
        return new_env

    def replace_level(self, values):
        self._level = values
        return self

    def __getslice__(self, levels_up, offset):
        this = self

        while levels_up > 0 and this != None:
            this = this._parent
            levels_up -= 1

        return this._level[offset]

    def __getitem__(self, i):
        print "called getitem", i

    def __repr__(self):
        return '[%r %r]' % (self._level, self._parent)
