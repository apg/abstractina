from abstractina.machines.secd import *


code = Cons(
    Cons('ldc', Cons(1, None)),
    Cons(
        Cons('ldc', Cons(2, None)),
        Cons(
            Cons('cons', None),
            None)))


machine = SECDMachine()
state = SECDState(TypedStack(), Environment(), code, Stack())
machine.run(state, step=True)
