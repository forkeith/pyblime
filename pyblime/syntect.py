from pyblime.pysyntect import *

NOOP = ScopeStackOp.noop()


def ScopeRegionIterator(ops, line):
    i, i2 = 0, 0

    while True:
        if i > len(ops):
            break

        i1 = len(line) if i == len(ops) else ops[i][0]
        substr = line[i2:i1]
        i2 = i1
        op = NOOP if i == 0 else ops[i - 1][1]
        i += 1
        yield (substr, op)
