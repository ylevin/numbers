import math

MAX_LENGTH = 300


class Operator:
    def __init__(self, name, apply, possible=lambda x, y: True):
        self.name = name
        self.apply = apply
        self.possible = possible


def check_pow(x, y, max_length=MAX_LENGTH):
    if y < 0 or (x == 0 and y == 0):
        return False
    if x == 0:
        return True
    return math.log10(abs(x)) * y < max_length


plus_op = Operator("+", lambda x, y: x + y)
minus_op = Operator("-", lambda x, y: x - y)
times_op = Operator("*", lambda x, y: x * y)
div_op = Operator("/", lambda x, y: x // y, lambda x, y: y != 0 and x % y == 0)
pow_op = Operator("**", lambda x, y: x ** y, check_pow)


def orders(n):
    if n == 1:
        yield [0]
    else:
        for item in orders(n - 1):
            for i in range(n):
                pos = n - i - 1
                yield item[:pos] + [n - 1] + item[pos:]


class Token:
    def __init__(self):
        self.parent = None

    def get_root(self):
        result = self

        while result.parent is not None:
            result = result.parent

        return result

    def to_string(self):
        raise NotImplemented

    def generate_results(self, operators):
        raise NotImplemented


class Constant(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def to_string(self):
        return str(self.value)

    def generate_results(self, operators):
        yield self.value


class Expression(Token):
    def __init__(self, left, right):
        super().__init__()
        self.left = left.get_root()
        self.right = right.get_root()
        self.operator = None
        self.left.parent = self
        self.right.parent = self

    def generate_results(self, operators):
        for right_value in self.right.generate_results(operators):
            for left_value in self.left.generate_results(operators):
                for op in operators:
                    self.operator = op
                    if op.possible(left_value, right_value):
                        yield op.apply(left_value, right_value)

    def to_string(self):
        return "({} {} {})".format(self.left.to_string(),
                                   self.operator.name,
                                   self.right.to_string())


def expressions(numbers, operators):
    count = len(numbers)
    op_length = count - 1
    for order in orders(op_length):
        tokens = [Constant(num) for num in numbers]
        for i in order:
            Expression(tokens[i], tokens[i + 1])
        root = tokens[0].get_root()

        for value in root.generate_results(operators):
            yield (root.to_string(), value)


def concat(d1, d2):
    return d1 * 10 + d2


def main():
    for item in expressions([1, 2, 3, 4, 5, 6, 7, 8, 9], [plus_op, minus_op, times_op, div_op, pow_op]):
        print("{} = {}".format(item[0], item[1]))


if __name__ == '__main__':
    main()
