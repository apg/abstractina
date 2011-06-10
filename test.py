from abstractina.backends.secd import SECDBackend
from abstractina.machines.secd import SECDMachine
from abstractina.data import cons2str, Cons, List
from abstractina.ast import *

compiler = SECDBackend()

s = AddOp(Const(1), Const(2))

c = compiler.compile(s)
print "Running", cons2str(c)
print c

machine = SECDMachine()
result = machine.go(c, step=True)
print result




s = If(EqOp(Const(1), Const(2)),
       Const(1), Const(2))
c = compiler.compile(s)
print "Running", cons2str(c)
print c

result = machine.go(c)
print result
