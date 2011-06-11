from abstractina.backends.secd import SECDBackend
from abstractina.machines.secd import SECDMachine
from abstractina.data import cons2str, Cons, List
from abstractina.ast import *

compiler = SECDBackend()

s = AddOp(Const(1), Const(2))

c = compiler.compile(s)
print "Running", cons2str(c)

machine = SECDMachine()
result = machine.go(c)
val, _ = result.S.pop('value')
print 'RESULT (expecting 3): ', val




s = If(EqOp(Const(1), Const(2)),
       Const(1), Const(2))
c = compiler.compile(s)
print "Running", cons2str(c)

result = machine.go(c)
val, _ = result.S.pop('value')
print 'RESULT (expecting 2): ', val



s = Apply(Lambda(['x', 'y'], AddOp(Var(1, 1, 'x'), Var(1, 2, 'y'))), 
          [Const(5), Const(5)])
c = compiler.compile(s)
print "Running", cons2str(c)
val, _ = result.S.pop('value')
print 'RESULT (expecting 10): ', val
