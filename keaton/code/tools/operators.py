

import numpy as np


class Field:
    """TEST CLASS FOR DEBUGGING"""

    def __init__(self, name=None):

        if name is None:
            name = 'F' + str(np.random.randint(10,99))

        self.name = name
        self.data = np.zeros(10)

    def __repr__(self):

        return self.name

    def __neg__(self):

        return Negative(self)

    def __add__(self, other):

        return Add(self, other)

    def __radd__(self, other):

        return Add(other, self)

    def __sub__(self, other):

        return Subtract(self, other)

    def __rsub__(self, other):

        return Subtract(other, self)

    def __mul__(self, other):

        return Multiply(self, other)

    def __rmul__(self, other):

        return Multiply(other, self)


class Operator:

    name = 'Operator'
    n_args = None

    def __init__(self, *args):

        # Inputs
        self.args = list(args)

        # Check number of arguments
        if self.n_args:
            if len(args) != self.n_args:
                raise ValueError("Wrong number of arguments.")

    def __repr__(self):

        # Represent as "name(arguments)"
        r_op = self.name
        r_args = [a.__repr__() for a in self.args]

        return r_op + '(' + ', '.join(r_args) + ')'

    def __neg__(self):

        return Negative(self)

    def __add__(self, other):

        return Add(self, other)

    def __radd__(self, other):

        return Add(other, self)

    def __sub__(self, other):

        return Subtract(self, other)

    def __rsub__(self, other):

        return Subtract(other, self)

    def __mul__(self, other):

        return Multiply(self, other)

    def __rmul__(self, other):

        return Multiply(other, self)

    def field_set(self):

        # Recursively collect Field arguments
        fields = set()
        for a in self.args:
            if isinstance(a, Field):
                fields.add(a)
            elif isinstance(a, Operator):
                fields.update(a.field_set())

        return fields

    def attempt_evaluation(self):

        # Recursively attempt evaluation of operator arguments
        for i, a in enumerate(self.args):
            if isinstance(a, Operator):
                a_eval = a.attempt_evaluation()
                if a_eval:
                    # Replace argument with its evaluation
                    self.args[i] = a_eval
                else:
                    # Cannot evaluate if arguments cannot be evaluated
                    return None

        # Check layout and space conditions
            # if conditions are satisfied:
                # return self.evaluate()
            # else:
                # return None

        # FOR DEBUGGING*********************************************************
        return self.evaluate()

    def evaluate(self):

        # This method must be implemented in subclasses.
        # Assume all Operator args have been evaluated to Fields.
        # Should return a Field object.

        raise NotImplementedError()


class Negative(Operator):

    name = 'Neg'
    n_args = 1

    def __str__(self):

        # Print as "-arg"
        s_arg = self.args[0].__str__()

        return '-' + s_arg

    def evaluate(self):

        out = Field()
        out.data[:] = -self.args[0].data

        return out


class Add(Operator):

    name = 'Add'
    n_args = 2

    def __str__(self):

        # Print as "arg1 + arg2"
        s_args = [a.__str__() for a in self.args]

        # Parenthesize arithmetic operations
        for i, a in enumerate(self.args):
            if isinstance(a, (Negative, Add, Subtract, Multiply)):
                s_args[i] = '(' + s_args[i] + ')'

        return ' + '.join(s_args)

    def get_data(self, arg):

        if isinstance(arg, Field):
            return arg.data
        elif np.isscalar(arg):
            return arg
        else:
            raise TypeError("Unsupported type: %s" %type(arg).__name__)

    def evaluate(self):

        out = Field()
        out.data[:] = self.get_data(self.args[0]) + self.get_data(self.args[1])

        return out


class Subtract(Operator):

    name = 'Sub'
    n_args = 2

    def __str__(self):

        # Print as "arg1 - arg2"
        s_args = [a.__str__() for a in self.args]

        # Parenthesize arithmetic operations
        for i, a in enumerate(self.args):
            if isinstance(a, (Negative, Add, Subtract, Multiply)):
                s_args[i] = '(' + s_args[i] + ')'

        return ' - '.join(s_args)

    def get_data(self, arg):

        if isinstance(arg, Field):
            return arg.data
        elif np.isscalar(arg):
            return arg
        else:
            raise TypeError("Unsupported type: %s" %type(arg).__name__)

    def evaluate(self):

        out = Field()
        out.data[:] = self.get_data(self.args[0]) - self.get_data(self.args[1])

        return out


class Multiply(Operator):

    name = 'Mult'
    n_args = 2

    def __str__(self):

        # Print as "arg1 * arg2"
        s_args = [a.__str__() for a in self.args]

        # Parenthesize arithmetic operations
        for i, a in enumerate(self.args):
            if isinstance(a, (Negative, Add, Subtract, Multiply)):
                s_args[i] = '(' + s_args[i] + ')'

        return ' * '.join(s_args)

    def get_data(self, arg):

        if isinstance(arg, Field):
            return arg.data
        elif np.isscalar(arg):
            return arg
        else:
            raise TypeError("Unsupported type: %s" %type(arg).__name__)

    def evaluate(self):

        out = Field()
        out.data[:] = self.get_data(self.args[0]) * self.get_data(self.args[1])

        return out
