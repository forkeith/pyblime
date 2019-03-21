def clamp(x, min_v, max_v):
    return max(min_v, min(x, max_v))


class Edit():

    def __init__(self, view):
        self.view = view
        self.selections = view.sel()
        self.view.beginUndoAction()

    def replace(self, r_orig, text):
        r = Region(max(0, r_orig.begin()), min(r_orig.end(), len(self.view.text())))

        self.view("SCI_DELETERANGE", r.begin(), r.size())
        self.view.insertAt(text, *self.view.lineIndexFromPosition(r.begin()))

        max_size = len(self.view.text())
        offset = len(text) - r.size()
        sels = []
        pt = r.begin()
        # pt2 = r.end()

        for s in self.selections:
            if s.begin() == r_orig.begin() and s.end() == r_orig.end():
                newr = Region(r_orig.begin(), r_orig.end() + offset)
            elif r.contains(s):
                newr = Region(
                    clamp(s.a + offset, pt, max_size),
                    clamp(s.b + offset, pt, max_size)
                )
            else:
                newr = Region(
                    clamp(s.a + offset, pt, max_size) if pt <= s.a else s.a,
                    clamp(s.b + offset, pt, max_size) if pt <= s.b else s.b
                )

            if newr not in sels:
                sels.append(newr)

        self.selections = sels

    def erase(self, r):
        pt = r.begin()
        offset = len(r)
        self.view("SCI_DELETERANGE", pt, offset)

        sels = []
        for s in self.selections:
            newr = Region(
                s.a if s.a <= pt else max(s.a - offset, pt),
                s.b if s.b <= pt else max(s.b - offset, pt)
            )
            if newr not in sels:
                sels.append(newr)

        self.selections = sels

    def insert(self, pt, text):
        offset = len(text)
        self.view.insertAt(text, *self.view.lineIndexFromPosition(pt))

        sels = []
        for s in self.selections:
            newr = Region(
                s.a if s.a <= pt else s.a + offset,
                s.b if s.b <= pt else s.b + offset
            )
            if newr not in sels:
                sels.append(newr)

        self.selections = sels

    def flush(self):
        view = self.view
        view.add_selections(self.selections)
        view.endUndoAction()


class Region(object):
    __slots__ = ['a', 'b']

    def __init__(self, a, b=None):
        if b is None:
            b = a
        self.a = a
        self.b = b

    def __str__(self):
        return "(" + str(self.a) + ", " + str(self.b) + ")"

    def __repr__(self):
        return "(" + str(self.a) + ", " + str(self.b) + ")"

    def __len__(self):
        return self.size()

    def __eq__(self, rhs):
        return isinstance(rhs, Region) and self.a == rhs.a and self.b == rhs.b

    def __lt__(self, rhs):
        lhs_begin = self.begin()
        rhs_begin = rhs.begin()

        if lhs_begin == rhs_begin:
            return self.end() < rhs.end()
        else:
            return lhs_begin < rhs_begin

    def empty(self):
        return self.a == self.b

    def begin(self):
        if self.a < self.b:
            return self.a
        else:
            return self.b

    def end(self):
        if self.a < self.b:
            return self.b
        else:
            return self.a

    def size(self):
        return abs(self.a - self.b)

    def contains(self, x):
        if isinstance(x, Region):
            return self.contains(x.a) and self.contains(x.b)
        else:
            return x >= self.begin() and x <= self.end()

    def cover(self, rhs):
        a = min(self.begin(), rhs.begin())
        b = max(self.end(), rhs.end())

        if self.a < self.b:
            return Region(a, b)
        else:
            return Region(b, a)

    def intersection(self, rhs):
        if self.end() <= rhs.begin():
            return Region(0)
        if self.begin() >= rhs.end():
            return Region(0)

        return Region(max(self.begin(), rhs.begin()), min(self.end(), rhs.end()))

    def intersects(self, rhs):
        lb = self.begin()
        le = self.end()
        rb = rhs.begin()
        re = rhs.end()

        return (
            (lb == rb and le == re) or
            (rb > lb and rb < le) or (re > lb and re < le) or
            (lb > rb and lb < re) or (le > rb and le < re)
        )
