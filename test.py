from abstractina.backends.secd import SECDBackend
from abstractina.machines.secd import SECDMachine
from abstractina.data import cons2str, Cons, List
from abstractina.ast import *
from abstractina.environment import NameLookupEnvironment

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
c = compiler.compile(s, NameLookupEnvironment())
print "Running", cons2str(c)

result = machine.go(c)
val, _ = result.S.pop('value')
print 'RESULT (expecting 2): ', val



s = Apply(Lambda(['x', 'y'], AddOp(Var('x'), Var('y'))), 
          [Const(5), Const(5)])
c = compiler.compile(s, env=NameLookupEnvironment())
print "Running", cons2str(c)
print c
result = machine.go(c, step=False)
val, _ = result.S.pop('value')
print 'RESULT (expecting 10): ', val
