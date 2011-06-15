class IndexedEnvironment(object):
    """An environment that works with De Brujin Indexes"""

    __slots__ = ('_level', '_parent',)

    def __init__(self, values=None, parent=None):
        self._parent = parent
        self._level = values or []

    def new_level(self, values=None):
        new_env = IndexedEnvironment(values=values, parent=self)
        return new_env

    def replace_level(self, values):
        self._level = values
        return self

    def __getslice__(self, levels_up, offset):
        this = self
        levels_up -= 1 # we start at 0, but they start at 1
        while levels_up > 0 and this != None:
            this = this._parent
            levels_up -= 1

        print "LOOKING UP %d in %r" % (offset, this._level)
        return this._level[offset - 1]

    def __getitem__(self, i):
        print "called getitem", i

    def __repr__(self):
        return '[%r %r]' % (self._level, self._parent)


Environment = IndexedEnvironment


class NameLookupEnvironment(object):
    """An environment that can lookup by name"""

    __slots__ = ('_level', '_parent',)

    def __init__(self, names=None, parent=None):
        self._parent = parent
        self._level = names or []

    def new_level(self, names=None):
        new_env = NameLookupEnvironment(names=names, parent=self)
        return new_env

    def __getitem__(self, name):
        this = self
        level = 0
        offset = -1
        
        while this != None:
            this = this._parent
            if name in self._level:
                offset = self._level.index(name) + 1
                level += 1
                break

        # 1 based, offset of -1 is nameerror
        return (level, offset)

    def __repr__(self):
        return '[%r %r]' % (self._level, self._parent)
