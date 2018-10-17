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
pow_op = Operator("^", lambda x, y: x ** y, check_pow)


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

    def need_update(self):
        if self.parent is not None:
            self.parent.need_update()

    def get_root(self):
        result = self

        while result.parent is not None:
            result = result.parent

        return result

    def get_expressions(self):
        return []

    def to_string(self):
        raise NotImplemented


class Constant(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get(self):
        return self.value

    def to_string(self):
        return str(self.value)


class Expression(Token):
    def __init__(self, left, right, operator):
        super().__init__()
        self.left = left.get_root()
        self.right = right.get_root()
        self.operator = operator
        self.value = None

        self.left.parent = self
        self.right.parent = self

    def get(self):
        if self.value is None:
            left_value = self.left.get()
            right_value = self.right.get()

            possible = right_value is not math.nan and left_value is not math.nan
            possible = possible and self.operator.possible(left_value, right_value)

            if possible:
                self.value = self.operator.apply(left_value, right_value)
            else:
                self.value = math.nan

        return self.value

    def need_update(self):
        self.value = None
        super().need_update()

    def set_operator(self, operator):
        if self.operator is not operator:
            self.operator = operator
            self.need_update()

    def get_expressions(self):
        return [self] + self.left.get_expressions() + self.right.get_expressions()

    def to_string(self):
        return "({} {} {})".format(self.left.to_string(),
                                   self.operator.name,
                                   self.right.to_string())


def expressions(numbers, operators):
    count = len(numbers)
    op_count = len(operators)
    op_length = count - 1
    for order in orders(op_length):
        tokens = [Constant(num) for num in numbers]
        for i in order:
            Expression(tokens[i], tokens[i + 1], None)
        root = tokens[0].get_root()
        exps = root.get_expressions()
        for i in range(op_count ** op_length):
            value = i
            for k in range(op_length):
                exps[k].set_operator(operators[value % op_count])
                value //= op_count

            result_value = root.get()

            if result_value is not math.nan:
                yield (root.to_string(), result_value)


def concat(d1, d2):
    return d1 * 10 + d2


def main():
    for item in expressions([1, 2, 3, 4, 5, 6, 7, 8, 9], [plus_op, minus_op, times_op, div_op]):
        if item[1] == 2018:
            print("{} = {}".format(item[0], item[1]))
            break


if __name__ == '__main__':
    main()
