def hello():
    return "hello world"


def factorize(value):
    powers = []
    for i in range(2, value):
        while value % i == 0:
            powers.append(str(i))
            value /= i
    return '*'.join(powers)


def is_prime(value):
    import math
    for i in range(2, int(math.sqrt(value))):
        if value % i == 0:
            return "1"
    return "0"
