import sys

from PyQt5.Qt import *  # noqa

from pyblime import *  # noqa

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
