pyblime
=========

## Usage

- pip install -r requirements.txt
- `echo %cd% > <location_your_python>/Lib/site-packages/pyblime.pth`

## Editor Usage

    import sys
    from pathlib import Path
    from PyQt5.Qt import *  # noqa
    from pyblime import *  # noqa

    if __name__ == "__main__":
        data_path = Path(__file__).parent / "../data"
        app = QApplication(sys.argv)
        ex = PyblimeEditor(data_path / "st_build_3149/syntax")
        ex.load_theme(data_path / "st_build_3149/themes/Monokai.tmTheme")
        ex.load_file(__file__)
        ex.resize(800,600)
        ex.show()
        sys.exit(app.exec_())

