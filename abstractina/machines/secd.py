from collections import namedtuple

from abstractina.data import Cons, cons2list, cons2str
from abstractina.machines import AbstractMachine
from abstractina.exceptions import HaltException, UnknownInstructionError
from abstractina.environment import Environment
from abstractina.stack import TypedStack, Stack

SECDState = namedtuple('MachineState', 'S E C D')
Closure = namedtuple('Closure', 'frame env')
Instruction = namedtuple('Instruction', 'op_code args')


class SECDState(object):
    """Ensures things are kept with consistent types"""

    __slots__ = ('_S', '_E', '_C', '_D')

    def __init__(self, S, E, C, D):
        self.S = S
        self.E = E
        self.C = C
        self.D = D

    def _get_S(self):
        return self._S

    def _set_S(self, s):
        if not isinstance(s, TypedStack):
            raise TypeError("S must be a TypedStack")
        self._S = s

    S = property(_get_S, _set_S)

    def _get_E(self):
        return self._E

    def _set_E(self, e):
        if not isinstance(e, Environment):
            raise TypeError("E must be an Environment")
        self._E = e

    E = property(_get_E, _set_E)

    def _get_C(self):
        return self._C

    def _set_C(self, c):
        self._C = c

    C = property(_get_C, _set_C)

    def _get_D(self):
        return self._D

    def _set_D(self, d):
        if not isinstance(d, Stack):
            raise TypeError("D must be a Stack")
        self._D = d

    D = property(_get_D, _set_D)

    def __repr__(self):
        return "<SECD State: { S: %r } { E: %r } { C: %r } { D: %r }>" % \
            (self._S, self._E, self._C, self._D)

instructions = {
    'n': 'NIL',
    'd': 'DUM',
    'c': 'LDC',
    'l': 'LD',
    'f': 'LDF',
    'j': 'JOIN',
    's': 'SEL',
    'a': 'AP',
    'p': 'RAP',
    'r': 'RET',
    '.': 'CONS',
    '(': 'CAR',
    ')': 'CDR',
    '+': 'ADD',
    '*': 'MUL',
    '-': 'SUB',
    '/': 'DIV',
    '=': 'EQ',
    '!': 'HALT',
    'nil': 'NIL',
    'dum': 'DUM',
    'ldc': 'LDC',
    'ld': 'LD',
    'ldf': 'LDF',
    'join': 'JOIN',
    'sel': 'SEL',
    'ap': 'AP',
    'ret': 'RET',
    'cons': 'CONS',
    'car': 'CAR',
    'cdr': 'CDR',
    'add': 'ADD',
    'mul': 'MUL',
    'sub': 'SUB',
    'div': 'DIV',
    'eq': 'EQ',
    'HALT': 'HALT',
}


class SECDMachine(AbstractMachine):

    def execute(self, instruction, state, verbose=False):
        op_code = instruction
        if op_code in ('!', 'HALT'): # halt state
            raise HaltException()
        operator = self.get_operator(op_code)
        return operator(state)

    def step(self, instruction, state):
        state = self.execute(instruction, state, verbose=True)
        self.dump_state(state)
        raw_input('> press enter to continue <')
        return state

    def get_operator(self, op_code):
        name = instructions.get(op_code, None)
        if not name:
            raise UnknownInstructionError("No instruction named '%s'" \
                                              % op_code)
        return getattr(self, 'op_%s' % name)

    def run(self, state, step=False):
        try:
            if step:
                executer = self.step
            else:
                executer = self.execute

            while state.C is not None:
                instruction = state.C.car
                state = executer(instruction,
                                 SECDState(state.S,
                                              state.E,
                                              state.C.cdr,
                                              state.D))
        except HaltException:
            print ".HALTED"

        return state

    def go(self, code, step=False):
        state = SECDState(TypedStack(), Environment(), code, Stack())
        return self.run(state, step)

    def dump_state(self, state):
        print 'S: ', state.S
        print 'E: ', state.E
        print 'C: ', state.C
        print 'C exp: ', cons2str(state.C)
        print 'D: ', state.D

    def op_NIL(self, state):
        """nil pushes a nil pointer onto the stack"""
        new_stack = state.S.push('value', None)
        return SECDState(new_stack, state.E, state.C.cdr, state.D)

    def op_LDC(self, state):
        """ldc pushes a constant argument onto the stack"""
        constant = state.C.car
        new_stack = state.S.push('value', constant)
        return SECDState(new_stack, state.E, state.C.cdr, state.D)

    def op_LD(self, state):
        """ld pushes the value of a variable onto the stack.

        The variable is indicated by the argument, a pair. The pair's car
        specifies the level, the cdr the position. So "(1 . 3)" gives the
        current function's (level 1) third parameter.
        """
        var = state.C.car
        value = state.E[var.car:var.cdr]
        new_stack = state.S.push('value', value)
        return SECDState(new_stack, state.E, state.C.cdr, state.D)

    def op_LDF(self, frame, state):
        """ldf takes one list argument representing a function. It
        constructs a closure (a pair containing the function and the current
        environment) and pushes that onto the stack.
        """
        new_stack = state.S.push('closure', Closure(frame, state.E,))
        return SECDState(new_stack, state.E, state.C, state.D)

    def op_SEL(self, state):
        """sel expects two list arguments, and pops a value from the stack.

        The first list is executed if the popped value was non-nil,
        the second list otherwise. Before one of these list pointers
        is made the new C, a pointer to the instruction following sel
        is saved on the dump.
        """
        conditional, new_stack = state.S.pop('value')

        new_dump = state.D.push(state.C.cdr.cdr)

        consequent = state.C.car
        alternate = state.C.cdr.car

        new_code = alternate if conditional is None else consequent
        return SECDState(new_stack, state.E, new_code, state.D)

    def op_JOIN(self, state):
        """join pops a list reference from the dump and makes this the
        new value of C.

        This instruction occurs at the end of both alternatives of a
        sel.
        """
        new_code, new_dump = state.D.pop()
        return SECDState(state.S, state.E, new_code, new_dump)

    def op_AP(self, state):
        """ap pops a closure and a list of parameter values from the stack.

        The closure is applied to the parameters by installing its
        environment as the current one, pushing the parameter list in
        front of that, clearing the stack, and setting C to the
        closure's function pointer. The previous values of S, E, and
        the next value of C are saved on the dump.
        """
        new_dump = state.D.push(state.S).push(state.E).push(state.C)
        closure, new_stack = state.S.pop('closure')
        parameters, new_stack = state.S.pop('value')
        if not isinstance(parameters, Cons):
            raise ValueError("top of stack expected to be a cons")
        param_list = cons2list(parameters)

        new_stack = state.S.reset()
        new_env = closure.env.new_level(param_list)
        return SECDState(new_stack, new_env, closure[0], new_dump)

    def op_RAP(self, state):
        """rap works like ap, only that it replaces an occurrence of a
        dummy environment with the current one, thus making recursive
        functions possible
        """
        new_dump = state.D.push(state.S).push(state.E).push(state.C)
        closure, new_stack = state.S.pop('closure')
        parameters, new_stack = state.S.pop('value')
        if not isinstance(parameters, Cons):
            raise ValueError("top of stack expected to be a cons")
        param_list = cons2list(parameters)

        new_stack = state.S.reset()
        new_env = closure[1].replace_level(param_list)
        return SECDState(new_stack, new_env, closure[0], new_dump)

    def op_RET(self, state):
        """ret pops one return value from the stack, restores S, E, and C
        from the dump, and pushes the return value onto the now-current stack.
        """
        old_code, new_dump = state.D.pop()
        old_env, new_dump = state.D.pop()
        old_stack, new_dump = state.D.pop()
        ret_val, _ = state.S.pop()
        new_old_stack = old_stack.push(ret_val)
        return SECDState(new_old_stack, old_env, old_code, new_dump)

    def op_DUM(self, state):
        """dum pushes a "dummy", an empty list, in front of the environment
        list.
        """
        new_env = state.E.new_level()
        return SECDState(state.S, new_env, state.C.cdr, state.D)

    def op_CONS(self, state):
        """cons pushes a cons to the stack made from the 2 top values of the
        stack.

        The car of the cons will be the top value on the stack.
        The cdr of the cons will be the second value on the stack.
        """
        car, s = state.S.pop('value')
        cdr, s = s.pop('value')

        new_stack = s.push('value', Cons(car, cdr))
        return SECDState(new_stack, state.E, state.C.cdr, state.D)

    def op_CAR(self, state):
        """car pushes the car of a the cons on the top of the stack
        """
        cons, s = state.S.pop('value')
        if not isinstance(cons, Cons):
            raise ValueError("top value of the stack not a cons")
        new_stack = s.push('value', cons.car)
        return SECDState(new_stack, state.E, state.C.cdr, state.D)

    def op_CDR(self, state):
        """car pushes the car of a the cons on the top of the stack
        """
        cons, s = state.S.pop('value')
        if not isinstance(cons, Cons):
            raise ValueError("top value of the stack not a cons")
        new_stack = s.push('value', cons.cdr)
        return SECDState(new_stack, state.E, state.C.cdr, state.D)

    def op_ADD(self, state):
        """add pushes the sum of the top two values back onto the stack
        """
        op1, s = state.S.pop('value')
        op2, s = s.pop('value')
        if not (isinstance(op1, int) and isinstance(op2, int)):
            raise ValueError("can't take the sum of non-integers")
        new_stack = s.push('value', op1 + op2)
        return SECDState(new_stack, state.E, state.C, state.D)

    def op_SUB(self, state):
        """add pushes the sum of the top two values back onto the stack
        """
        op1, s = state.S.pop('value')
        op2, s = s.pop('value')
        if not (isinstance(op1, int) and isinstance(op2, int)):
            raise ValueError("can't take the difference of non-integers")
        new_stack = s.push('value', op1 - op2)
        return SECDState(new_stack, state.E, state.C, state.D)

    def op_MUL(self, state):
        """mul pushes the product of the top two values back onto the stack
        """
        op1, s = state.S.pop('value')
        op2, s = s.pop('value')
        if not (isinstance(op1, int) and isinstance(op2, int)):
            raise ValueError("can't take the product of non-integers")
        new_stack = s.push('value', op1 + op2)
        return SECDState(new_stack, state.E, state.C, state.D)

    def op_DIV(self, state):
        """add pushes the sum of the top two values back onto the stack
        """
        op1, s = state.S.pop('value')
        op2, s = s.pop('value')
        if not (isinstance(op1, int) and isinstance(op2, int)):
            raise ValueError("can't take the quotient of non-integers")
        new_stack = s.push('value', op1 / op2)
        return SECDState(new_stack, state.E, state.C, state.D)

    def op_EQ(self, state):
        """eq pushes a non nil value to the stack if the top 2 stack
        values are equal. pushes nil (None) otherwise.
        """
        op1, s = state.S.pop('value')
        op2, s = s.pop('value')
        if op1 == op2:
            new_value = 1
        else:
            new_value = None
        new_stack = s.push('value', new_value)
        return SECDState(new_stack, state.E, state.C, state.D)
