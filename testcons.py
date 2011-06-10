from abstractina.read import read
from abstractina.data import cons2str
from abstractina.machines.secd import *



program = """
;; cons two numbers together
((ldc 1)
 (ldc 2)
 (cons)) ;;; should get (2 . 1)
"""

code = read(program)
machine = SECDMachine()
state = SECDState(TypedStack(), Environment(), code, Stack())
final = machine.run(state, step=True)

val, _ = final.S.pop('value')
print cons2str(val)


#
# "(cons 1 2)" ->

# (ldc 2) (ldc 1) (cons)
