import StringIO
import sys

from abstractina.data import Cons


__putback_tokens = []

def putback(token):
    __putback_tokens.append(token)

def next_token(inp):
    token = ''

    if __putback_tokens:
        return __putback_tokens.pop()

    # eat spaces
    ch = inp.read(1)
    while ch.isspace():
        if ch == '':
            sys.stderr.write("error: EOF reached in next_token()\n")
            sys.exit(1)
        ch = inp.read(1)

    # are we a comment?
    while ch == ';':
        inp.readline() # read til newline
        ch = inp.read(1)

    # are we a delimiter?
    #    if ch in ('(', ')', "'"):
    if ch in ('(', ')'):
        return ch

    token += ch

    while True:
        ch = inp.read(1)
        if ch == '':
            sys.stderr.write("error: EOF reached in next_token()-\n")
            sys.exit(1)

        #        if ch in ('(', ')', "'"):
        if ch in ('(', ')') or ch.isspace():
            pos = inp.tell()
            inp.seek(pos - 1)
            return token

        token += ch

    # never get here.
    return token


def read_object(inp):
    token = next_token(inp)
    if token == '(':
        return read_list(inp)
#    if token == "'":
#        return Cons("quote", Cons(read_object(inp), nil))
    if token.isdigit(): # we don't consider negative numbers
        return int(token)
    return token


def read_list(inp):
    token = next_token(inp)
    if token == ')':
        return None
    
    if token == '.':
        tmp = read_object(inp)
        if next_token(inp) != ')':
            sys.stderr.write("error: improper use of dotted list notation.")
            sys.exit(1)

        return tmp
    putback(token)
    return Cons(read_object(inp), read_list(inp))


def read(inp=sys.stdin):
    if isinstance(inp, str):
        return read_object(StringIO.StringIO(inp))
    return read_object(inp)

