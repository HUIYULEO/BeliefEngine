from sympy import *
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Not
import itertools
from math import isclose
from Resolution import PL_Resolution

class Belief:
    def __init__(self, formula, value=None) -> None:
        self.formula = to_cnf(formula)
        self.value = value

class BeliefBase:
    ''' initially belief base is empty '''
    def __init__(self):
        self.beliefs = [] #list of Belief objects
        self.decrease_constant = 0.1

    def _removeBelief(self, formula):
        for i, b in enumerate(self.beliefs):
            if b.formula == formula:
                self.beliefs.pop(i)

    def expand(self, belief: Belief):
        if PL_Resolution([], ~belief.formula):
            #it is contraddiction -> should be ignored
            return

        if belief.value is None:
            symbols_set = belief.formula.free_symbols
            for b in self.beliefs:
                if symbols_set.intersection(b.formula.free_symbols):
                    b.value -= b.value*self.decrease_constant
            belief.value = 1

        self._removeBelief(belief.formula)
        self.beliefs.append(belief)

    def clear_belief_base(self):
        self.beliefs = [] # may be it can be dict or a set?


    def getclauses(self):
        return [belief.formula for belief in self.beliefs]

    

    """       
    def arrangeBeliefs(self):

            result = []
            prev_order = None

            for belief in self.beliefBase:
                if prev_order is None:
                    result.append(belief)
                    prev_order = belief.order
                    continue

                if isclose(belief.order,
                           prev_order):  
                    result.append(belief)

                else:
                    yield prev_order, result
                    result = [belief]
                    prev_order = belief.order

            yield prev_order, result

    def degree(self, newBelief):

            if PL_Resolution([], newBelief):

            base = []
            for order, r in self.arrangeBeliefs():  
                base += [b.newBelief for b in r]
                if PL_Resolution(base, newBelief):
                    return order
            return 0  # otherwise return 0

    def revision(self, newBelief, order, add=True):
            formula = to_cnf(newBelief) 
            negFormula = Not(formula)
            deg = self.degree(formula)

            if 0 <= order <= 1:
                if not PL_Resolution([], negFormula):
                    # Is the new belief inconsistent
                    if PL_Resolution([], formula):
                        # Is it a tautology 
                        order = 1
                    elif order <= deg:
                        self.contraction(formula, order)
                    else:
                        self.contraction(negFormula, 0)
                        self.expansion(formula, order, False)

                    if add:
                        self.add(formula, order)
            else:
                order = False 
'
    def revision(self, newBelief):
        formula = to_cnf(newBelief)
        negFormula = Not(formula)
        self.contraction(negFormula)
        self.expansion(newBelief)'''
    """        
    ''' contraction'''
    def contraction(self, belief):
        newBelief = to_cnf(belief)
        for b in self.beliefBase:
            if b == newBelief:
                self.beliefBase.remove(newBelief)

    def print_belief(self):
        if self.beliefs:
            for b in self.beliefs:
                print(b.formula, b.value)
        else:
            print("The belief base is empty")
    
    #Not sure we need this class. Maybe is helpful only when we do the part with plausible belief
    """      
    class Belief:
        ''' it gets the formula to convert it into cnf form '''
        def __init__(self, formula) -> None:
            self.formula = formula
            self.newcnf = to_cnf(formula)
    """

if __name__ == "__main__":
    x, y = symbols('x,y')

    bb = BeliefBase()
    bb.expand(Belief(x))
    bb.expand(Belief(x|y))
    bb.expand(Belief(x & Not(x))) #contraddiction is not added
    bb.expand(Belief(x)) #only the duplicate with the highest order is kept
    bb.expand(Belief(y, 0.3)) #add belief with specific value
    bb.print_belief()
