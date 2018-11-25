from typing import *
import math
import random
import sys

from ArithmeticExpression import ArithmeticExpression, Operations

class Datfuscator():

    def __init__(self):
        pass

    
    def obfuscate(self, integer: int):
        pass

    def to_multinomial(self, n: int, n_terms: int=3) -> ArithmeticExpression:

        assert n_terms > 0

        result = ArithmeticExpression(n)

        for i in range(n_terms - 1):
            last_term = result.pop()
            last_sign = result[-1] if len(result) != 0 else None

            result.extend(self.to_binomial(last_term))

            if last_sign == Operations.SUBTRACTION:
                
                if result[-2] == Operations.ADDITION:
                    result[-2] = Operations.SUBTRACTION
                else:
                    result[-2] = Operations.ADDITION
        
        result.simplify()
        return result


    def to_binomial(self, n: int) -> ArithmeticExpression:
        
        rand = random.randint(-9223372036854775808, 9223372036854775807)

        if bool(random.getrandbits(1)):
            return ArithmeticExpression(rand, '-', rand - n)
        else:
            return ArithmeticExpression(-rand, '+', rand + n)



if __name__ == "__main__":

    d = Datfuscator()
    result = d.to_multinomial(400, 5)

    print( repr((5 * result + 6).complexify()))
    