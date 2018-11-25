from typing import *
from enum import Enum
import collections
import random
from itertools import chain
import math

class Operations(Enum):
        ADDITION = '+'
        SUBTRACTION = '-'
        MULTIPLICATION = '*'
        DIVISION = '/'
        EXPONENTIATION = '**'

class ArithmeticExpression(collections.MutableSequence):
    """
    Class to represent an arithmetic expression.
    Implements multiple abstractions to easily operate on said expression.
    """
    # Temporary safety setting until proper algorithm is implemented
    VALIDATE_BEFORE_UNSAFE_EVAL = True

    def __init__(self, *values):
        self.list = list()

        self.extend(list(values))

    def check(self, value):
        if not isinstance(value, (int, str, ArithmeticExpression, Operations) ):
            raise TypeError(value)
        if type(value) is str:
            try:            
                value = Operations(value)
            except ValueError:
                raise ValueError(f"String '{value}' not whitelisted") from None
        return value

    def eval(self):
        return self.unsafe_eval() # TODO fix

    def unsafe_eval(self) -> int:

        if self.VALIDATE_BEFORE_UNSAFE_EVAL:
            for i, element in enumerate(self):
                # This makes all elements go through the "proper" route, 
                # to prevent security concerns from coming up when you alter self.list directly without __setitem__
                self[i] = element
        return eval(str(self))

    def simplify(self):
        self.simplify_sign()
        return self

    def simplify_sign(self):
        """
        Attempt to simplify expression

        For now, only sign simplifications are made. 
        For example: 9 - -2 = 9 + 2 and -5 + -2 = -5 - 2
        """

        i = 0
        while True:
            if self[i] == Operations.SUBTRACTION and isinstance(self[i+1], (int, ArithmeticExpression)):
                if self[i + 1] < 0:
                    self[i] = Operations.ADDITION
                    self[i + 1] = abs(self[i + 1])
                i += 2
            elif self[i] == Operations.ADDITION and isinstance(self[i+1], (int, ArithmeticExpression)):
                if self[i + 1] < 0:
                    self[i] = Operations.SUBTRACTION
                    self[i + 1] = abs(self[i + 1])
                i += 2
            else:
                i += 1
            if i >= len(self):
                break
        return self
    
    def complexify_sign(self):
        """
        Attempt to complexify expression.
        That is to say, do the inverse of .simplify_sign(),
        and deliberately create as many complex sign combinations as possible. 
        For example: -5 - 2 = -5 + -2 and 9 + 2 = 9 - -2 
        """

        i = 0
        while True:
            if self[i] == Operations.ADDITION and isinstance(self[i+1], (int, ArithmeticExpression)):
                if self[i + 1] > 0:       
                    self[i] = Operations.SUBTRACTION
                    self[i + 1] = -abs(self[i + 1])
                i += 2
            elif self[i] == Operations.SUBTRACTION and isinstance(self[i+1], (int, ArithmeticExpression)):
                if self[i + 1] > 0:
                    self[i] = Operations.ADDITION
                    self[i + 1] = -abs(self[i + 1])
                i += 2
            else:
                i += 1
            if i >= len(self):
                break

        return self

    def complexify(self):
        self.complexify_sign()
        return self

    def group_terms(self):
        """
        Convert the expression to a new expression with the first dimension exclusively consisting of alternating addition and subtraction operations and `ArithmeticExpression`s 
        """

        if not self.is_superficial_sum():
            if len(self) < 1:
                self.list = ArithmeticExpression(*self)
            return self
        
        def append_expression(to_append_to, to_append):
            if isinstance(to_append, ArithmeticExpression) and len(to_append) == 1:
                    for elem in to_append:
                        to_append_to.append(elem)
            else:
                to_append_to.append(to_append)
        self.simplify()
        result, term = ArithmeticExpression(), ArithmeticExpression()
        for element in self:
            if element == Operations.ADDITION or element == Operations.SUBTRACTION:
                # New term reached
                result.extend([term, element])
                term = ArithmeticExpression()
            else:
                if isinstance(element, ArithmeticExpression):
                    element.group_terms()
                append_expression(term, element)
        # Be sure to not forget the dangling last term
        result.extend(ArithmeticExpression(term))
        self.list = result.list[:]
        return self
    def shuffle_terms(self):
        """
        Shuffle the terms of the expression in a random order.
        """
        ((1) + ((((2) + (5)) * ((1) + (3)))))
        self.group_terms()
        terms = [[Operations.ADDITION, self[0]]]
        for i in range(1, len(self), 2):
            terms.append([self[i], self[i + 1]])
        random.shuffle(terms) # DevSkim: ignore DS148264, no cryptographically secure randomization needed
        self.list = list(chain.from_iterable(terms))
        self.simplify()
        if self[0] == Operations.SUBTRACTION:
            self[1].negate()
        self.pop(0)
        return self

    def is_superficial_sum(self) -> bool:
        """
        Shallowly (non-recursive) checks if expression consist of a sum or not 
        """

        return Operations.ADDITION in self or Operations.SUBTRACTION in self

    def is_sum(self) -> bool:
        """
        Checks if expression consists of a sum or not.
        """

        for element in self:
            if element == Operations.ADDITION or element == Operations.SUBTRACTION:
                return True
            elif isinstance(element, ArithmeticExpression) and element.is_sum():
                return True
        return False

    def insert(self, i, v):
        v = self.check(v)
        self.list.insert(i, v)

    def copy(self) -> 'ArithmeticExpression':
        return ArithmeticExpression(*self)

    def n_terms():
        return math.ceil(len(self.group_terms()) / 2)

    def __setitem__(self, i, v):
        v = self.check(v)
        self.list[i] = v

    def __str__(self):
        representation = ' '.join([str(element.value if isinstance(element, Enum) else element) for element in self])
        if len(self) > 1:
            return '(' + representation + ')'
        return representation

    def __repr__(self):
        return f"{self} = {self.eval()}"

    def __abs__(self):

        copy = self.copy()
        if copy < 0:
            return -copy
        return copy
    
    def __mul__(self, other):
        
        if not isinstance(other, ArithmeticExpression):
            other = ArithmeticExpression(other)

        copy = self.copy()
        copy.group_terms()
        if not copy.is_superficial_sum():
            copy[0] = ArithmeticExpression(other, Operations.MULTIPLICATION, copy[0])
            return copy
        for i in range(0, len(copy), 2):
            current = copy[i]
            if isinstance(current, ArithmeticExpression):
                copy[i] *= other
        copy.simplify()
        return copy

    def __add__(self, other):
        copy = self.copy()
        if not isinstance(other, ArithmeticExpression):
            other = ArithmeticExpression(other)
        copy.extend([Operations.ADDITION, other])
        return copy
    
    def __radd__(self, other):
        copy = self.copy()
        if not isinstance(other, ArithmeticExpression):
            other = ArithmeticExpression(other)
        other.extend([Operations.ADDITION, copy])
        return other

    def __neg__(self):
        return self * -1

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.eval() == other
    
    def __lt__(self, other):
        return self.eval() < other
    
    def __gt__(self, other):
        return self.eval() > other
    
    def __le__(self, other):
        return self.eval() <= other
    
    def __ge__(self, other):
        return self.eval() >= other

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]
        
if __name__ == "__main__":

    l = ArithmeticExpression(1, "+",  2, "*", ArithmeticExpression(1, '+', 3))
    #l.as_equation()
    print((l * l))
    