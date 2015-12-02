# -*- coding: utf-8 -*-
"""
Author: Sean Shahkarami

This program is a demonstration on how you can implement `basic`
regular expressions using the concept of a `derivative`. This is
inspired by the nice paper `Regular-expression derivatives reexamined`
by Scott Owens, John Reppy and Aaron Turon.
"""


def seq(r, s):
    if r is False or s is False:
        return False
    if r is True:
        return s
    if s is True:
        return r
    return ('.', r, s)


def plus(r, s):
    if r is True or s is True:
        return True
    if r is False:
        return s
    if s is False:
        return r
    return ('+', r, s)


def neg(r):
    if isinstance(r, bool):
        return not r
    return ('~', r)


def star(r):
    if isinstance(r, bool):
        return True
    return ('*', r)


def maybe(r):
    return plus(r, '')


def times(r, n):
    if n == 1:
        return r
    return seq(r, times(r, n-1))


def nullable(re):
    if isinstance(re, bool):
        return re
    if isinstance(re, str):
        return re == ''
    if isinstance(re, tuple) and re[0] == '.':
        return nullable(re[1]) and nullable(re[2])
    if isinstance(re, tuple) and re[0] == '+':
        return nullable(re[1]) or nullable(re[2])
    if isinstance(re, tuple) and re[0] == '~':
        return not nullable(re[1])
    if isinstance(re, tuple) and re[0] == '*':
        return True
    return False


def deriv(a, re):
    if isinstance(re, bool):
        return re
    if isinstance(re, str):
        return a == re
    if isinstance(re, tuple) and re[0] == '.':
        return plus(seq(deriv(a, re[1]), re[2]),
                    seq(nullable(re[1]), deriv(a, re[2])))
    if isinstance(re, tuple) and re[0] == '+':
        return plus(deriv(a, re[1]),
                    deriv(a, re[2]))
    if isinstance(re, tuple) and re[0] == '~':
        return neg(deriv(a, re[1]))
    if isinstance(re, tuple) and re[0] == '*':
        return seq(deriv(a, re[1]), ('*', re[1]))
    return False


def match(s, re):
    for a in s:
        re = deriv(a, re)
    return nullable(re)


# complete matches
print(deriv('a', 'a'))
print(deriv('a', 'b'))
print(deriv('a', neg('a')))
print(deriv('a', neg('b')))

# partial matching
print(deriv('a', seq(seq('a', 'b'), 'c')))

# more complicated matches
print(deriv('a', star(seq('a', 'b'))))
print(deriv('c', star(seq('a', 'b'))))
print(match('ab', star(seq('a', 'b'))))

# Degenerate example I found in the article `Regular Expressions
# can be Simplex and Fast` by Russ Cox. The example is:
#
#  n times  n times
# a?.....a?a.......a
#
n = 30
re = seq(times(maybe('a'), n), times('a', n))
print(match('a' * n, re))
