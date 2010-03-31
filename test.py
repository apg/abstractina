from secd.machine import *

code = [
    ('ldc', (1,)),
    ('ldc', (2,)),
    ('cons',),
]

machine = SECDMachine()
state = MachineState(Stack(), Environment(), code, Stack())
machine.run(state)
