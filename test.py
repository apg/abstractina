from abstractina.machines.secd import *

code = [
    ('ldc', (1,)),
    ('ldc', (2,)),
    ('cons',),
]

machine = SECDMachine()
state = SECDState(TypedStack(), Environment(), code, Stack())
machine.run(state, step=True)
