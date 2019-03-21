import sys
from pathlib import Path

from PyQt5.Qt import *  # noqa

from pyblime import *  # noqa


def center(widget, x=0, y=0):
    frame_geometry = widget.frameGeometry()
    screen = QApplication.desktop().screenNumber(
        QApplication.desktop().cursor().pos())
    center_point = QApplication.desktop().screenGeometry(
        screen).center()

    frame_geometry.moveCenter(center_point + QPoint(x, y))
    widget.move(frame_geometry.topLeft())


class DockFiles(QTreeView):

    file_changed = pyqtSignal(str)

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = QFileSystemModel()
        self.model.setRootPath(f"{str(path)[0:2]}/")
        self.setModel(self.model)
        self.setRootIndex(self.model.index(str(path)))
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    def currentChanged(self, current, previous):
        self.file_changed.emit(self.model.fileInfo(current).absoluteFilePath())


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        # Paths
        data_path = Path(__file__).parent / "../data"
        themes_path = data_path / "st_build_3149/themes"
        syntax_path = data_path / "st_build_3149/syntax"
        files_path = data_path / "testfiles"

        # Central widget
        self.view = View(syntax_path)
        self.view.syntax_changed.connect(self.set_window_title)
        self.view.theme_changed.connect(self.set_window_title)
        self.setCentralWidget(self.view)

        # Dock files
        tree = DockFiles(files_path)
        self.dock_files = QDockWidget("Files", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_files)
        self.dock_files.setWidget(tree)
        tree.file_changed.connect(self.view.load_file)

        # Dock themes
        tree = DockFiles(themes_path)
        self.dock_themes = QDockWidget("Themes", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_themes)
        self.dock_themes.setWidget(tree)
        tree.file_changed.connect(self.view.load_theme)

    def set_window_title(self):
        ed = self.view
        path = ed.path
        syntax_name = ed.syntax.name if ed.syntax else None
        theme_name = ed.theme.name if ed.theme else None
        self.setWindowTitle(f"{path}  -  {syntax_name}  -  {theme_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.setWindowTitle(__file__)
    ex.resize(800, 600)
    center(ex)
    ex.show()
    sys.exit(app.exec_())
