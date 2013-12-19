from math import log, sqrt, floor

class CacheIt(object):
    def __init__(self, func):
        self.func = func
        self.__cache = {}

    def __call__(self, *args, **kwargs):
        frozen_args = tuple(args)
        frozen_kwargs = tuple([(key, value) for key, value in kwargs.iteritems()])
        cache_key = (frozen_args, frozen_kwargs)
        if cache_key not in self.__cache:
            self.__cache[cache_key] = self.func(*args, **kwargs)
        return self.__cache[cache_key]

def factorize(number):
    orig_number = number
    limit = int(floor(sqrt(number)))
    ret = []
    prime_pointer = 0
    while number > 1:
        counter = 0
        cprime = __primes[prime_pointer]
        while number % cprime == 0:
            counter += 1
            number /= cprime
        if counter > 0:
            ret.append((cprime, counter))
        prime_pointer += 1
    # print "factors for %s are: %s" %  (orig_number, ret)
    return ret
    
def balanced_product(number):
    orig_number = number
    factors = factorize(number)
    fl = len(factors)
    stack = [([0 for _ in xrange(fl)], 0)]
    max_value = number
    best_one, best_other = number, 1
    was = set()
    
    while stack:
        cstack, cpointer = stack.pop()
        while cpointer < fl:
            if cstack[cpointer] + 1 <= factors[cpointer][1]:
                nstack = cstack[:]
                nstack[cpointer] += 1
                tuple_form = tuple(nstack)
                if tuple_form not in was:
                    stack.append((nstack, cpointer))
                    was.add(tuple_form)
            else:
                one, other = 1, 1
                for index, (base, exp) in enumerate(factors):
                    one *= base**(exp - cstack[index])
                    other *= base**cstack[index]
                cmax = max(one, other)
                if cmax < max_value:
                    max_value = cmax
                    best_one, best_other = one, other
            cpointer += 1
    #print "best balanced product for %s is: %s, %s" % (number, best_one, best_other)
    return best_one, best_other

def to_number(iterable):
    acc = 0
    for exp, digit in enumerate(iterable):
        acc += 10**exp * digit
    return acc 

def solve(digits):
    assert digits > 0
    cpal = [9 for _ in xrange(digits * 2)]
    pointer = digits - 1
    fdigits = float(digits)
    while pointer > -1:
        value = to_number(cpal)
        one, other = balanced_product(value)
        if log(one) / log(10) < fdigits and log(other) / log(10) < fdigits:
            print "one: %s, other: %s" % (one, other)
            return value
        cpal[pointer] -= 1
        cpal[-1 - pointer] -= 1
        while pointer > -1 and cpal[pointer] == -1:
            cpal[pointer] = 9
            cpal[-1 - pointer] = 9
            pointer -= 1
            if pointer == -1:
                break
            cpal[pointer] -= 1
            cpal[-1 - pointer] -= 1
        if pointer != -1:
            pointer = digits - 1
    return -1

__primes = None

def read_primes():
    global __primes
    with open("primes.txt", "r") as f:
        lines = f.readlines()
        __primes = [int(line.strip()) for line in lines]

def complexity(iterable):
    ret = 1
    for _, exp in iterable:
        ret *= exp + 1
    return ret

def get_complexity(top):
    max_value = 0
    max_complexity = 0
    for i in xrange(1, top + 1):
        curr_complexity = complexity(factorize(i))
        if curr_complexity > max_complexity:
            max_value = i
            max_complexity = curr_complexity
    return (max_value, max_complexity)

if __name__ == "__main__":
    from sys import argv
    read_primes()
    print solve(int(argv[1]))
