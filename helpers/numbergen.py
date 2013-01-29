import random
import unittest
import sys


def gen_integer_array(numInts, low, high):
    random.seed()
    rands = []
    for i in range(0, numInts):
        rnd = random.randrange(low, high)
        rands.append(rnd)
    return rands


def gen_nonzero_integer_array(numInts, low, high):
    random.seed()
    rands = []
    for i in range(0, numInts):
        k = gen_integer(low, high)
        while k == 0:
            k = gen_integer()
        rands.append(k)
    return rands


def gen_integer(low, high):
    random.seed()
    return random.randrange(low, high)

def gen_nonzero_integer(low, high):
    random.seed()
    result = 0
    while result == 0:
        result = random.randrange(low, high)
    return result


class NumberGenTest(unittest.TestCase):
    def setUp(self):
        pass

    def are_all_elements_in_range(self, intArray, low, high):
        for i in intArray:
            if i > high or i < low:
                print i, low, high
                return False
        return True

    def test_standard_input(self):
        for size in range(1, 10):
            integers = gen_integer_array(size, -10, 10)
            self.assertTrue(len(integers) == size)
            self.assertTrue(self.are_all_elements_in_range(integers, -10, 10))

    def test_extreme_input(self):
        for size in range(1, 10):
            integers = gen_integer_array(size, -999999999, 999999999)
            self.assertTrue(len(integers) == size)

if __name__ == "__main__":
    mode = sys.argv[1:]
    # unittest does not like more than 1 item in sys.argv. It just fails
    del sys.argv[1:]
    if len(mode) > 0:
        if mode[0] == "test":
            unittest.main()
