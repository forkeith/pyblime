
from PyQt5.Qt import *  # noqa

from pysyntect import *  # noqa


def qt_color(c):
    return QColor(c.r, c.g, c.b)


class ThemeWidget(QTableWidget):

    def __init__(self, path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_theme(path)

    def load_theme(self, path):
        if not path:
            return

        theme = ThemeSet.get_theme(str(path))
        settings = theme.settings
        colors = {}
        attrs = [v for v in dir(theme.settings) if not v.startswith("__")]
        for k in attrs:
            try:
                colors[k] = qt_color(getattr(settings, k))
            except Exception as e:
                pass

        self.setColumnCount(2)
        self.setRowCount(len(colors))

        index = 0
        for k, v in colors.items():
            item_text = QTableWidgetItem(f"{k}")
            item_col = QTableWidgetItem()
            item_col.setBackground(v)
            self.setItem(index, 0, item_text)
            self.setItem(index, 1, item_col)
            index += 1
