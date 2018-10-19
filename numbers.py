import math

MAX_LENGTH = 300


class Operator:
    def __init__(self, display, priority, apply, possible=lambda x, y: True):
        self.display = display
        self.apply = apply
        self.priority = priority
        self.possible = possible

    def __str__(self):
        return self.display


def check_pow(x, y, max_length=MAX_LENGTH):
    if y < 0 or (x == 0 and y == 0):
        return False
    if x == 0:
        return True
    try:
        return math.log10(abs(x)) * y < max_length
    except ArithmeticError:
        return False


plus_op = Operator("+", 1, lambda x, y: x + y)
minus_op = Operator("-", 1, lambda x, y: x - y)
times_op = Operator("*", 2, lambda x, y: x * y)
div_op = Operator("/", 2, lambda x, y: x // y, lambda x, y: y != 0 and x % y == 0)
pow_op = Operator("**", 3, lambda x, y: x ** y, check_pow)


def keep_parentheses(op, parent_op, is_left):
    if op is None:
        return False
    if parent_op == plus_op:
        return False
    if parent_op == minus_op and (is_left or op.priority > minus_op.priority):
        return False
    if parent_op == times_op and (op == times_op or op.priority >= times_op.priority):
        return False
    if parent_op == div_op and (op.priority > div_op.priority or (is_left and op.priority == div_op.priority)):
        return False
    if parent_op == pow_op and op == pow_op and not is_left:
        return False

    return True


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
        self.operator = None

    def get_root(self):
        result = self

        while result.parent is not None:
            result = result.parent

        return result

    def generate_results(self, operators):
        raise NotImplemented


class Constant(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def generate_results(self, operators):
        yield self.value


class Expression(Token):
    def __init__(self, left, right):
        super().__init__()
        self.left = left.get_root()
        self.right = right.get_root()
        self.left.parent = self
        self.right.parent = self

    def generate_results(self, operators):
        for right_value in self.right.generate_results(operators):
            for left_value in self.left.generate_results(operators):
                for op in operators:
                    self.operator = op
                    if op.possible(left_value, right_value):
                        yield op.apply(left_value, right_value)

    def __str__(self):
        left = self.left
        right = self.right
        if keep_parentheses(self.left.operator, self.operator, True):
            left = "({})".format(left)
        if keep_parentheses(self.right.operator, self.operator, False):
            right = "({})".format(right)
        return "{} {} {}".format(left, self.operator, right)


def expressions(numbers, operators):
    count = len(numbers)
    op_length = count - 1
    if op_length == 0:
        yield (numbers[0], lambda: str(numbers[0]))
    else:
        for order in orders(op_length):
            tokens = [Constant(num) for num in numbers]
            for i in order:
                Expression(tokens[i], tokens[i + 1])
            root = tokens[0].get_root()

            for value in root.generate_results(operators):
                yield (value, lambda: str(root))


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
    make_table(1000)
