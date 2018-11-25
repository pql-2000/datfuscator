from typing import *
from ArithmeticExpression import Operations

class ExpressionEvalulator:
    """
    A class to safely evaluate `ArithmeticExpression`s, without any kind of security concern, 
    like which would be the case using eval(), exec() or similar
    """

    @staticmethod
    def evaluate(expression: 'ArithmeticExpression') -> int:
        raise NotImplementedError()
