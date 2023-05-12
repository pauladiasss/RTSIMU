import ast
import operator
import math
import sys
from typing import Any, Generator, Iterable, Tuple

if sys.version_info >= (3, 10):
    from itertools import pairwise
else:
    from itertools import tee

    def pairwise(iterable: Iterable) -> zip:
        """
        group an iterable into pairs of adjacent elements (s -> (s0,s1), (s1,s2), (s2, s3), ...)
        :param iterable: the iterable to group.
        :type iterable: Iterable
        :return: an iterator of tuples of adjacent elements.
        """
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)


def safe_eval(s: str) -> Any:
    """
    Evaluate a string containing a Python expression.
    adapted from https://stackoverflow.com/a/68732605 by user @jay-m.
    :param s: the string to evaluate.
    :type s: str
    :return: the result of the evaluation.
    :rtype: Any
    """

    def checkmath(x, *args):
        """
        Check if the function is in math and call it.
        :param x: function name.
        :param args: arguments to pass to the function.
        :return: the result of the function.
        """
        if x not in [o for o in dir(math) if "__" not in o]:
            raise SyntaxError(f"Unknown func {x}()")
        fun = getattr(math, x)
        return fun(*args)

    bin_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.Call: checkmath,
        ast.BinOp: ast.BinOp,
    }

    un_ops = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.UnaryOp: ast.UnaryOp,
    }

    bool_ops = {
        ast.And: all,
        ast.Or: any,
    }

    cmp_ops = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge
    }

    names = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
    }

    ops = tuple(bin_ops) + tuple(un_ops) + tuple(bool_ops) + tuple(cmp_ops)

    tree = ast.parse(s, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.value
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                return names[node.id]
            else:
                raise SyntaxError(f"Bad syntax, {type(node)}")
        elif isinstance(node, ast.BinOp):
            if isinstance(node.left, (ops, ast.Name)):
                left = _eval(node.left)
            else:
                left = node.left.value
            if isinstance(node.right, (ops, ast.Name)):
                right = _eval(node.right)
            else:
                right = node.right.value
            return bin_ops[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.operand, (ops, ast.Name)):
                operand = _eval(node.operand)
            else:
                operand = node.operand.value
            return un_ops[type(node.op)](operand)
        elif isinstance(node, ast.BoolOp):
            values = [_eval(v) for v in node.values]
            return bool_ops[type(node.op)](values)
        elif isinstance(node, ast.Call):
            args = [_eval(x) for x in node.args]
            r = checkmath(node.func.id, *args)
            return r
        elif isinstance(node, ast.Compare):
            comparators = [_eval(node.left)] + [_eval(c) for c in node.comparators]
            return all(cmp_ops[type(op)](left, right) for op, (left, right) in zip(node.ops, pairwise(comparators)))
        else:
            raise SyntaxError(f"Bad syntax, {type(node)}")

    return _eval(tree)