import sys
from pathlib import Path

from PyQt5.Qt import *  # noqa

from pyblime import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    st_path = Path(__file__).parent / "../data/st_build_3149"
    w = ThemeWidget(str(st_path / "themes/Monokai.tmTheme"))
    w.show()

    sys.exit(app.exec_())
