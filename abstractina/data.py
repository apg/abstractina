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
    buffer = []
    buffer.append("(")

    buffer.append(obj2str(c.car))

    if not isinstance(c.cdr, Cons):
        buffer.append(' . ')
        buffer.append(obj2str(c.cdr))
    else:
        buffer.append(' ')
        buffer.append(cons2str(c.cdr))

    buffer.append(')')

    return ''.join(buffer)
    
