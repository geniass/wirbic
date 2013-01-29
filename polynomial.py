import sympy
import sys
import unittest
from helpers import numbergen, weblatex


def gen_factorised_polynomial(constants, coefficient=1, var="x"):
    """'constants' is a list of constants that would make up the constant term, i.e., in
    (x+1)(x-4) constants would be [1, -4]. Coefficient is the coefficient of
    the term with the highest power"""
    if coefficient == 0:
        coefficient = 1
    x = sympy.Symbol(var)
    expression = 1
    for c in constants:
        expression = expression * ((coefficient * x) + c)
        coefficient = 1
    return expression


def gen_random_factorised_polynomial(numTerms, low, high):
    """Generate a random factorised polynomial. numTerms is the polynomial's
    order + 1, e.g., numTerms=3 could make (x + 4)(x + 2)(x + 2). low and high
    are the minimum and maximum values of the coefficients."""
    return gen_factorised_polynomial(
            numbergen.gen_integer_array(numTerms, low, high),
                                    numbergen.gen_nonzero_integer(low, high))


def gen_factorable_polynomial(constants, coefficient=1, var="x"):
    """'constants' is a list of constants that make up the constant term, i.e., in
    (x+1)(x-4) constants would be [1, -4]. Coefficient is the coefficient of
    the term with the highest power"""
    return gen_factorised_polynomial(constants, coefficient, var).expand()


def gen_random_factorable_polynomial(numTerms, low, high):
    """Generate a random factorable polynomial. numTerms is the polynomial's
    order + 1, e.g., numTerms=3 could make 3x^3 + 4x^2 - 2x +3. low and high
    are the minimum and maximum values of the coefficients."""
    return gen_factorable_polynomial(
            numbergen.gen_integer_array(numTerms, low, high),
                                    numbergen.gen_nonzero_integer(low, high)) 


def gen_random_factorable_polynomial_equal_zero(numTerms, low, high):
    """Generates a random, factorable polynomial and sets it equal to zero"""
    return sympy.Eq(gen_random_factorable_polynomial(numTerms, low, high), 0)


def gen_random_factorised_polynomial_equal_zero(numTerms, low, high):
    """Generates a random, factorised polynomial and sets it equal to zero"""
    return sympy.Eq(gen_random_factorised_polynomial(numTerms, low, high), 0)


def factorise(expression):
    return expression.factor()


def solve(expression, var="x"):
    """Solves the given expression, and returns the solutons in the form [x == a, x == b]"""
    x = sympy.Symbol(var)
    zeros = sympy.solve(expression, x)
    return [sympy.Eq(x, z) for z in zeros]


def latex_polynomial(expression):
    """Returns the LaTex representation of the given polynomial expression"""
    return weblatex.escape_latex_for_web(sympy.latex(expression))


def latex_solutions(solutions, var="x"):
    """Takes solutions in the form [x == a, x == b] and returns their LaTex representation"""
    return weblatex.escape_latex_for_web(
            '\ or\ '.join([sympy.latex(s) for s in solutions]))


class PolynomialTests(unittest.TestCase):

    def testPolynomial(self):
        constants = [3, -2, 0]
        x = sympy.Symbol("x")
        gen_polynomial = gen_factorable_polynomial(constants, "x")
        true_polynomial = x**3 + x**2 - 6*x
        self.failUnless(gen_polynomial == true_polynomial)

    def test_latex_polynomial(self):
        x = sympy.Symbol("x")
        gen_polynomial = x**3 + x**2 - 6*x
        gen_latex = latex_polynomial(gen_polynomial)
        print gen_latex
        true_latex = """\[x^{3} + x^{2} - 6 x\]"""
        self.failUnless(gen_latex == true_latex)


if __name__ == "__main__":
    mode = sys.argv[1:]
    # unittest does not like more than 1 item in sys.argv. It just fails
    del sys.argv[1:]
    if len(mode) > 0:
        if mode[0] == "test":
            unittest.main()
