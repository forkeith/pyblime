import sys

from PyQt5.Qt import *  # noqa

from pyblime import *

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    view = View()

    tests_insert = [
        (
            '0123456789',
            [(10, 6)],
            '0abcde123456789',
            [(15, 11)],
            lambda: view.insert(edit, 1, "abcde"),
        ),
        (
            '0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(0, 10), (22, 32)],
            '01234abcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(0, 15), (27, 37)],
            lambda: view.insert(edit, 5, "abcde"),
        ),
        (
            '01234abcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(27, 37), (49, 59), (71, 81), (93, 103)],
            '01234abcdeabcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(32, 42), (54, 64), (76, 86), (98, 108)],
            lambda: view.insert(edit, 5, "abcde"),
        ),
        (
            '01234abcdeabcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(0, 20)],
            '01234abcdeabcdeabcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(0, 25)],
            lambda: view.insert(edit, 5, "abcde"),
        ),
        (
            '01234abcdeabcdeabcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(0, 2), (8, 4), (15, 11), (25, 21), (30, 34)],
            '01234abcdeabcdeabcdeabcde56789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n0123456789\n',
            [(0, 2), (13, 4), (20, 16), (30, 26), (35, 39)],
            lambda: view.insert(edit, 5, "abcde"),
        )
    ]

    tests_erase = [
        (
            '0123456789\n',
            [(0, 1)],
            '06789\n',
            [(0, 1)],
            lambda: view.erase(edit, Region(1, 6)),
        ),
        (
            '0123456789\n',
            [(11, 5)],
            '06789\n',
            [(6, 1)],
            lambda: view.erase(edit, Region(1, 6)),
        ),
        (
            '0123456789\n',
            [(2, 0), (3, 5), (10, 7)],
            '06789\n',
            [(1, 0), (1, 1), (5, 2)],
            lambda: view.erase(edit, Region(1, 6)),
        ),
        (
            '0123456789\n',
            [(0, 10)],
            '06789\n',
            [(0, 5)],
            lambda: view.erase(edit, Region(1, 6)),
        ),
        (
            '0123456789\n',
            [(10, 0)],
            '06789\n',
            [(5, 0)],
            lambda: view.erase(edit, Region(1, 6)),
        ),
        (
            '0123456789\n',
            [(0, 0)],
            '06789\n',
            [(0, 0)],
            lambda: view.erase(edit, Region(6, 1)),
        ),
        (
            '0123456789',
            [(0, 2), (3, 5)],
            '56789',
            [(0, 0)],
            lambda: view.erase(edit, Region(0, 5))
        ),
        (
            '0123456789',
            [(2, 10)],
            '56789',
            [(0, 5)],
            lambda: view.erase(edit, Region(0, 5))
        )
    ]
    tests_replace = [
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(5, 9), (10, 14), (15, 19)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(10, 14), (15, 19), (20, 24)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(2, 20)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(7, 25)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(0, 0), (4, 20)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(5, 5), (9, 25)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'abcdefghijk',
            [(0, 3), (5, 7), (9, 11)],
            'abcdefghijklm',
            [(2, 5), (7, 9), (11, 13)],
            lambda: view.replace(edit, Region(0, 11), "abcdefghijklm")
        ),
        (
            'abcdefghijk',
            [(0, 3), (5, 7), (9, 11)],
            'abcdefghi',
            [(0, 1), (3, 5), (7, 9)],
            lambda: view.replace(edit, Region(0, 11), "abcdefghi")
        ),
        (
            'abcdefghijk',
            [(0, 3), (5, 7), (9, 11)],
            'i',
            [(0, 0), (0, 1)],
            lambda: view.replace(edit, Region(0, 11), "i")
        ),
        (
            'abcde',
            [(0, 5)],
            'abcde',
            [(0, 5)],
            lambda: view.replace(edit, Region(0, 11), "abcde")
        ),
        (
            'abcde',
            [(5, 0)],
            'abce',
            [(4, 0)],
            lambda: view.replace(edit, Region(0, 11), "abce")
        ),
        (
            'abcde',
            [(5, 0)],
            'abc',
            [(3, 0)],
            lambda: view.replace(edit, Region(0, 11), "abc")
        ),
        (
            'abcde',
            [(5, 0)],
            'a',
            [(1, 0)],
            lambda: view.replace(edit, Region(0, 11), "a")
        ),
        (
            'abcde',
            [(5, 0)],
            '',
            [(0, 0)],
            lambda: view.replace(edit, Region(0, 11), "")
        ),
        (
            'xxxxxxxabcdexxxxxxxxxxxx',
            [(2, 0), (4, 9), (13, 19)],
            'xx',
            [(2, 0), (2, 2)],
            lambda: view.replace(edit, Region(2, 30), "")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4',
            [(0, 4)],
            'foo1\nfoo2\nfoo3\nfoo4',
            [(0, 4)],
            lambda: view.replace(edit, Region(0, 4), "foo1")
        ),
        (
            'foo1\nfoo2\nfoo\nfoo4',
            [(0, 4), (10, 13)],
            'foo\nfoo2\nfoo\nfoo4',
            [(0, 3), (9, 12)],
            lambda: view.replace(edit, Region(0, 4), "foo")
        ),
        (
            'foo\nfoo\nfo\nfoo',
            [(0, 3), (4, 7), (8, 10), (11, 14)],
            'fo\nfoo\nfo\nfoo',
            [(0, 2), (3, 6), (7, 9), (10, 13)],
            lambda: view.replace(edit, Region(0, 3), "fo")
        ),
        (
            'oo1\noo2\noo3\noo4',
            [(0, 0), (1, 1), (4, 4), (5, 5), (8, 8), (9, 9), (12, 12), (13, 13)],
            'oo1\noo2\noo3\noo4',
            [(0, 0), (1, 1), (4, 4), (5, 5), (8, 8), (9, 9), (12, 12), (13, 13)],
            lambda: view.replace(edit, Region(1, 1), "")
        ),
        (
            'oo1\noo2\noo3\noo4',
            [(0, 0), (1, 1), (4, 4), (5, 5), (8, 8), (9, 9), (12, 12), (13, 13)],
            'oo1\noo2\noo3\noo4',
            [(0, 0), (1, 1), (4, 4), (5, 5), (8, 8), (9, 9), (12, 12), (13, 13)],
            lambda: view.replace(edit, Region(0, 0), "")
        ),
        (
            'o\n\n\n',
            [(0, 0), (0, 1), (2, 2), (3, 3), (4, 4)],
            '\n\n\n',
            [(0, 0), (1, 1), (2, 2), (3, 3)],
            lambda: view.replace(edit, Region(0, 1), "")
        ),
        (
            '\n\n\n',
            [(0, 0), (1, 1), (2, 2), (3, 3)],
            '\n\n\n',
            [(0, 0), (1, 1), (2, 2), (3, 3)],
            lambda: view.replace(edit, Region(0, 0), "")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(20, 5)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(25, 10)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(3, 0)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(8, 5)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(4, 0)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(0, 9)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(0, 4)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(0, 9)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(3, 0)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(8, 5)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        ),
        (
            'hello',
            [(5, 0)],
            'xx',
            [(0, 2)],
            lambda: view.replace(edit, Region(5, 0), "xx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4',
            [(14, 10)],
            'foo1\nfoo2\nxx\nfoo4',
            [(10, 12)],
            lambda: view.replace(edit, Region(14, 10), "xx")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4',
            [(4, 0)],
            '>foo1<\nfoo2\nfoo3\nfoo4',
            [(0, 6)],
            lambda: view.replace(edit, Region(4, 0), ">foo1<")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4',
            [(0, 4)],
            '>foo1<\nfoo2\nfoo3\nfoo4',
            [(0, 6)],
            lambda: view.replace(edit, Region(0, 4), ">foo1<")
        ),
        (
            'foo1\nfoo2\nfoo3\nfoo4\n',
            [(0, 4)],
            'xxxxxxxxx\nfoo2\nfoo3\nfoo4\n',
            [(0, 9)],
            lambda: view.replace(edit, Region(0, 4), "xxxxxxxxx")
        )
    ]

    tests_failing = [
    ]

    tests = []
    tests += tests_insert
    tests += tests_erase
    tests += tests_replace
    tests += tests_failing

    for i, t in enumerate(tests):
        text_input = t[0]
        sels_input = t[1]
        text_output = t[2]
        sels_output = t[3]
        operation = t[4]

        view.setText(text_input)
        view.add_selections(sels_input)
        edit = Edit(view)
        operation()
        edit.flush()

        try:
            assert view.text() == text_output
        except Exception as e:
            print("Error text".center(80, '-'))
            print("Input Text:", text_input)
            print("Output Text:", view.text())
            print("Expected text:", text_output)

        try:
            assert [(r.a, r.b) for r in view.sel()] == sels_output
        except Exception as e:
            print("Error selection".center(80, '-'))
            print("Input selections:", sels_input)
            print("Output Selections:", list(view.sel()))
            print("Expected selections:", sels_output)
