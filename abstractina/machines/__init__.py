"""Abstract Machine base class
"""

class AbstractMachine(object):
    
    def execute(self, instruction, state, verbose=False):
        raise NotImplemented()
    
    def step(self, instruction, state):
        raise NotImplemented()

    def run(self, state):
        raise NotImplemented()
