"""
Author: Sean Shahkarami

This is a simple example implementation of adding a `peek` feature
to Python generators. It just maintains a queue of elements already
looked at and then requests more from the generator as needed.
"""


class lookahead(object):

    def __init__(self, generator):
        self.generator = generator
        self.queue = []

    def peek(self, k):
        assert k >= 0
        while len(self.queue) <= k:
            self.queue.append(next(self.generator))
        return self.queue[k]

    def __iter__(self):
        return self.generator

    def __next__(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return next(self.generator)

    def __repr__(self):
        return "(" + ", ".join(list(map(str, self.queue)) + ["..."]) + ")"


def nats():
    n = 0
    while True:
        yield n
        n += 1


g = lookahead(nats())

print("Peeking at next 3 elements.")
print(g.peek(2))
print(g.peek(1))
print(g.peek(0))
print(g)
print()

print("Taking the next item.")
print(next(g))
print(g)
print()

print("Take some more elements until queue is empty.")
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(g)
print()
