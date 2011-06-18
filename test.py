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
val, _ = result.S.pop()
print 'RESULT (expecting 3): ', val
assert val == 3

print
s = If(EqOp(Const(1), Const(2)),
       Const(1), Const(2))
c = compiler.compile(s, NameLookupEnvironment())
print "Running", cons2str(c)
result = machine.go(c)
val, _ = result.S.pop()
print 'RESULT (expecting 2): ', val
assert val == 2



print 
s = Apply(Lambda(['x', 'y'], AddOp(Var('x'), Var('y'))), 
          [Const(5), Const(6)])
c = compiler.compile(s, env=NameLookupEnvironment())
print "Running", cons2str(c)
print c
result = machine.go(c, step=False)
val, _ = result.S.pop()
print 'RESULT (expecting 11): ', val
assert val == 11

print
s = Apply(Lambda(['x', 'y'], SubOp(Var('x'), Var('y'))), 
          [Const(5), Const(6)])
c = compiler.compile(s, env=NameLookupEnvironment())
print "Running", cons2str(c)
print c
result = machine.go(c, step=False)
val, _ = result.S.pop()
print 'RESULT (expecting -1): ', val
assert val == -1

print
s = Let(['z'], [Const(6)],
        Let(['x', 'y'], [Const(3), Const(5)],
            AddOp(Var('z'), SubOp(Var('x'), Var('y')))))
c = compiler.compile(s, env=NameLookupEnvironment())
print "Running", cons2str(c)
print c
result = machine.go(c, step=False)
val, _ = result.S.pop()
print 'RESULT (expecting 4): ', val
assert val == 4


print
s = LetRec(['add', 'sub', 'addandsub1'], 
           [Lambda(['a', 'b'], AddOp(Var('a'), Var('b'))),
            Lambda(['a', 'b'], SubOp(Var('a'), Var('b'))),
            Lambda(['a', 'b'], 
                   SubOp(AddOp(Var('a'), Var('b')),
                         Const(1)))],
           Apply(Var('addandsub1'), [Const(10), Const(1)]))
c = compiler.compile(s, env=NameLookupEnvironment())
print "Running", cons2str(c)
print c
result = machine.go(c)
val, _ = result.S.pop()
print 'RESULT (expecting 10): ', val
assert val == 10
