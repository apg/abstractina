from collections import namedtuple

Cons = namedtuple('Cons', 'car cdr')

def List(*args):
    return reduce(lambda d, a: Cons(a, d), reversed(args), None)


def cons2list(c):
    """Does a flat mapcar across the cons starting at ``c``
    
    If c is not a proper list (e.g. the last cdr is not None), it will not
    be included.
    """
    out = []
    next = c
    while isinstance(next, Cons):
        out.append(next.car)
        next = next.cdr
    return out


def obj2str(o):
    if isinstance(o, int):
        return str(o)
    elif isinstance(o, str):
        return o
    elif o is None:
        return 'nil'
    elif isinstance(o, Cons):
        return cons2str(o)


def cons2str(c):
    if c is None:
        return "nil"

    buffer = []
    buffer.append("(")

    buffer.append(obj2str(c.car))

    t = c.cdr
    while isinstance(t, Cons):
        buffer.append(' ')
        buffer.append(obj2str(t.car))
        t = t.cdr
    else:
        if t:
            buffer.append(' . ')
            buffer.append(obj2str(t))

    buffer.append(')')

    return ''.join(buffer)
