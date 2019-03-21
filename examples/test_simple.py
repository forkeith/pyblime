import sys
from pathlib import Path

from PyQt5.Qt import *  # noqa

from pyblime import *  # noqa

if __name__ == "__main__":
    data_path = Path(__file__).parent / "../data"
    app = QApplication(sys.argv)
    view = View(data_path / "st_build_3149/syntax")
    view.load_theme(data_path / "st_build_3149/themes/Monokai.tmTheme")
    view.load_file(__file__)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())
