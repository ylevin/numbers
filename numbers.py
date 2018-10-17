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
            yield (value, lambda: root.to_string())


def concat_expressions(digits, operators):
    count = len(digits)
    for i in range(2 ** (count - 1)):
        numbers = [digits[0]]
        for k in range(count - 1):
            if i // (2 ** k) % 2 == 1:
                numbers[-1] = numbers[-1] * 10 + digits[k + 1]
            else:
                numbers += [digits[k + 1]]

        for item in expressions(numbers, operators):
            yield item


def make_table(n=100):
    all_numbers = dict()
    for value, get_exp_string in concat_expressions([1, 2, 3, 4, 5, 6, 7, 8, 9],
                                                    [plus_op, minus_op, times_op, div_op, pow_op]):
        if 0 <= value < n and value not in all_numbers:
            all_numbers[value] = get_exp_string()
            if len(all_numbers) == n:
                for k, v in all_numbers.items():
                    print("{} = {}".format(v, k))
                break


def find(n):
    for value, get_exp_string in concat_expressions([1, 2, 3, 4, 5, 6, 7, 8, 9],
                                                    [plus_op, minus_op, times_op, div_op, pow_op]):
        if value == n:
            return "{} = {}".format(get_exp_string(), value)


if __name__ == '__main__':
    find(10958)
