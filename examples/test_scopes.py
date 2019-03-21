import os
from pathlib import Path

from pyblime.syntect import *  # noqa


def commonprefix(s1, s2):
    return os.path.commonprefix([s1, s2])


def text_scopes(text, syntax):
    state = ParseState(syntax)
    stack = ScopeStack()

    i = 0
    for num_line, line in enumerate(text.splitlines(True)):
        ops = state.parse_line(line, ss)
        for (s, op) in ScopeRegionIterator(ops, line):
            stack.apply(op)
            if not s:
                continue
            for j in range(len(s)):
                print("{:<20}{:<80}{}".format(
                    repr(text[i]), repr(op), stack
                ))
                i += 1


def extract_regions(data):
    lst = [list(map(operator.itemgetter(1), g)) for k, g in groupby(enumerate(data), lambda v:v[0] - v[1])]
    return [(v[0], v[-1]) for v in lst]


if __name__ == '__main__':
    text = (Path(__file__).parent / "x.py").read_text()
    ss = SyntaxSet.load_defaults_newlines()
    syntax = ss.find_syntax_by_extension("py")
    scopes = text_scopes(text, syntax)
