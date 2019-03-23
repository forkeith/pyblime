from pathlib import Path

from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.Qt import *  # noqa

from pyblime.sublime_wrapper import *
from pyblime.syntect import *
from pyblime.utils import *


class ViewLexer(QsciLexerCustom):

    def __init__(self, syntax_set, syntax, theme, parent=None):
        super().__init__(parent)

        self.syntax_set = syntax_set
        self.syntax = syntax
        self.theme = theme
        self.settings = theme.settings
        self.st = set()
        self.dct = {}
        self.num_style = 0

    def defaultPaper(self, style):
        return qt_color(self.settings.background)

    def language(self):
        return self.syntax.name

    def styleText(self, start, end):
        self.startStyling(0)
        # t_start = time.time()
        self.h = HighlightLines(self.syntax, self.theme)
        for line in self.parent().text().splitlines(True):
            for style, token in self.h.highlight(line, self.syntax_set):
                if style not in self.st:
                    self.dct[style] = self.num_style
                    self.st.add(style)
                    self.setColor(qt_color(style.foreground), self.num_style)
                    self.setPaper(qt_color(style.background), self.num_style)
                    self.setFont(QFont("Consolas", 8, weight=QFont.Bold), self.num_style)

                    self.setStyling(len(token), self.num_style)
                    self.num_style += 1
                else:
                    self.setStyling(len(token), self.dct[style])
        # print("SyntaxHighlighting", start, end, time.time() - t_start)

    def description(self, style_nr):
        return str(style_nr)


class View(QsciScintilla):

    syntax_changed = pyqtSignal()
    theme_changed = pyqtSignal()

    # -------- MAGIC FUNCTIONS --------
    def __init__(self, syntax_path=None, parent=None):
        super().__init__(parent)

        # Set font defaults
        font = QFont()
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(8)
        font.setBold(True)
        self.setFont(font)

        # Set indentation defaults
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)

        self.setFolding(QsciScintilla.CircledFoldStyle)

        # Set caret defaults
        self.setCaretWidth(2)

        # Set multiselection defaults
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)

        # Set selection color defaults
        self.resetSelectionForegroundColor()

        # Margins
        self.setMarginsFont(font)
        # self.setMarginsBackgroundColor(QColor(39, 40, 34))
        # self.setMarginsForegroundColor(QColor(128, 128, 128))
        self.setMarginType(0, self.NumberMargin)
        self.setMarginWidth(0, "00000")

        # Syntect
        self.load_syntax_set(syntax_path)
        self.syntax = None
        self.theme = None
        self.path = None

    def __len__(self):
        return self.size()

    def __call__(self, prop, *args, **kwargs):
        args = [v.encode("utf-8") if isinstance(v, str) else v for v in args]
        kwargs = {
            k: (v.encode("utf-8") if isinstance(v, str) else v)
            for k, v in kwargs.items()
        }
        return self.SendScintilla(getattr(self, prop), *args, **kwargs)

    # -------- SUBLIME VIEW PUBLIC INTERFACE --------
    def add_regions(self, key, regions, scope, icon, flags):
        raise NotImplementedError

    def buffer_id(self):
        raise NotImplementedError

    def change_count(self):
        raise NotImplementedError

    def classify(self, point):
        raise NotImplementedError

    def command_history(self, index, modifying_only):
        raise NotImplementedError

    def em_width(self):
        raise NotImplementedError

    def encoding(self):
        raise NotImplementedError

    def erase(self, edit, region):
        edit.erase(region)

    def erase_regions(self, key):
        raise NotImplementedError

    def erase_status(self, key):
        raise NotImplementedError

    def expand_by_class(self, x, classes, separators):
        # x = point or region
        raise NotImplementedError

    def extract_scope(self, point):
        raise NotImplementedError

    def file_name(self):
        raise NotImplementedError

    def find(self, pattern, start_point, flags):
        raise NotImplementedError

    def find_all(self, pattern, flags, format, extractions):
        raise NotImplementedError

    def find_by_class(self, point, forward, classes, separators):
        raise NotImplementedError

    def find_by_selector(self, selector):
        raise NotImplementedError

    def fold(self, x):
        # x = regions or region
        raise NotImplementedError

    def full_line(self, x):
        # x = point or region
        raise NotImplementedError

    def get_regions(self, key):
        raise NotImplementedError

    def get_status(self, key):
        raise NotImplementedError

    def hide_popup(self):
        raise NotImplementedError

    def id(self, ):
        raise NotImplementedError

    def insert(self, edit, pt, string):
        edit.insert(pt, string)

    def is_auto_complete_visible(self):
        raise NotImplementedError

    def is_dirty(self):
        raise NotImplementedError

    def is_loading(self):
        raise NotImplementedError

    def is_popup_visible(self):
        raise NotImplementedError

    def is_primary(self):
        raise NotImplementedError

    def is_read_only(self):
        raise NotImplementedError

    def is_scratch(self):
        raise NotImplementedError

    def layout_extent(self):
        raise NotImplementedError

    def layout_to_text(self, vector):
        raise NotImplementedError

    def layout_to_window(self, vector):
        raise NotImplementedError

    def line(self, x):
        # x = point or region
        raise NotImplementedError

    def line_endings(self):
        raise NotImplementedError

    def line_height(self):
        raise NotImplementedError

    def lines(self, region):
        text = self.text()
        len_text = len(text)
        region = Region(
            clamp(region.begin(), 0, len_text),
            clamp(region.end() - 1, 0, len_text)
        )

        # Move a to the first character of the first line
        if region.a == len_text:
            return [Region(len_text, len_text)]

        if text[region.a] == "\n":
            region.a -= 1
        while True:
            if text[region.a] == "\n":
                region.a += 1
                break
            if region.a <= 0:
                break
            region.a -= 1

        # Move b to the last character of the last line
        while region.b < len_text and text[region.b] != "\n":
            if region.b >= len_text:
                break
            region.b += 1

        lst = []
        for i in range(region.begin(), region.end() + 1, 1):
            if i >= len_text:
                break
            c = text[i]
            if c == "\n":
                lst.append(i)

        a = region.begin()
        res = []
        for v in lst:
            res.append(Region(a, v))
            a = v + 1

        return res

    def match_selector(self, point, selector):
        raise NotImplementedError

    def name(self):
        raise NotImplementedError

    def overwrite_status(self):
        raise NotImplementedError

    def replace(self, edit, region, string):
        edit.replace(region, string)

    def reset_reference_document(self):
        raise NotImplementedError

    def rowcol(self, point):
        raise NotImplementedError

    def run_command(self, string, args):
        raise NotImplementedError

    def scope_name(self, point):
        raise NotImplementedError

    def score_selector(self, point, selector):
        raise NotImplementedError

    def sel(self):
        regions = []

        for i in range(self("SCI_GETSELECTIONS")):
            regions.append(Region(
                self("SCI_GETSELECTIONNANCHOR", i),
                self("SCI_GETSELECTIONNCARET", i)
            ))

        return sorted(regions)

    def set_encoding(self, encoding):
        raise NotImplementedError

    def set_line_endings(self, line_endings):
        raise NotImplementedError

    def set_name(self, name):
        raise NotImplementedError

    def set_overwrite_status(self, enabled):
        raise NotImplementedError

    def set_read_only(self, value):
        raise NotImplementedError

    def set_reference_document(self, reference):
        raise NotImplementedError

    def set_scratch(self, value):
        raise NotImplementedError

    def set_status(self, key, value):
        raise NotImplementedError

    def set_syntax_file(self, syntax_file):
        raise NotImplementedError

    def set_viewport_position(self, vector, animate):
        raise NotImplementedError

    def settings(self):
        raise NotImplementedError
    # def show(self, location, show_surrounds):
    #     raise NotImplementedError

    def show_at_center(self, location):
        raise NotImplementedError

    def show_popup(self, content, flags, location, max_width, max_height, on_navigate, on_hide):
        raise NotImplementedError

    def show_popup_menu(self, items, on_done, flags):
        raise NotImplementedError

    def size(self):
        return len(self.text())

    def split_by_newlines(self, region):
        raise NotImplementedError

    def style(self):
        raise NotImplementedError

    def style_for_scope(self, scope_name):
        raise NotImplementedError

    def substr(self, x):
        # x = point or region
        if isinstance(x, Region):
            return self.text()[x.begin():x.end()]
        else:
            s = self.text()[x:x + 1]
            if len(s) == 0:
                return "\x00"
            else:
                return s

    def symbols(self):
        raise NotImplementedError

    def text_point(self, row, col):
        raise NotImplementedError

    def text_to_layout(self, point):
        raise NotImplementedError

    def text_to_window(self, point):
        raise NotImplementedError

    def unfold(self, x):
        # x = regions or region
        raise NotImplementedError

    def update_popup(self, content):
        raise NotImplementedError

    def viewport_extent(self):
        raise NotImplementedError

    def viewport_position(self):
        raise NotImplementedError

    def visible_region(self):
        raise NotImplementedError

    def window(self):
        raise NotImplementedError

    def window_to_layout(self, vector):
        raise NotImplementedError

    def window_to_text(self, vector):
        raise NotImplementedError

    def word(self, x):
        # x = point or region
        raise NotImplementedError

    # -------- PUBLIC WRITE METHODS --------
    def clear_selections(self):
        self("SCI_CLEARSELECTIONS")

    def add_selection(self, i, r):
        if isinstance(r, list) or isinstance(r, tuple):
            r = Region(*r)

        anchor, caret = r.a, r.b

        if i == 0:
            self("SCI_SETSELECTION", caret, anchor)
        else:
            self("SCI_ADDSELECTION", caret, anchor)

    def add_selections(self, lst):
        self.clear_selections()

        for i, s in enumerate(lst):
            self.add_selection(i, s)

        # view("SCI_SETMAINSELECTION", -1)

    def load_syntax_set(self, syntax_path):
        if not syntax_path:
            return

        builder = SyntaxSetBuilder()
        builder.add_from_folder(str(syntax_path), False)
        self.ss = builder.build()

    def load_file(self, path):
        if not self.ss:
            raise Exception("load_syntax_set hasn't been called yet")
        try:
            path = Path(path)
            ext = path.suffix[1:]
            self.setText(path.read_text())
            self.path = path
            self.syntax = self.ss.find_syntax_by_extension(ext)
        except Exception as e:
            self.syntax = None

        self.syntax_changed.emit()
        self._reload_lexer()

    def load_theme(self, path):
        try:
            theme = ThemeSet.get_theme(str(path))
            self.theme = theme
        except Exception as e:
            self.theme = None

        self.syntax_changed.emit()
        self._reload_lexer()

    # -------- PRIVATE METHODS --------
    def _set_color(self, method_name, col):
        if not col:
            return

        getattr(self, method_name)(qt_color(col))

    def _reload_lexer(self):
        if not self.syntax or not self.theme:
            self.setLexer(None)
            return

        settings = self.theme.settings

        # self._set_color("setCallTipsBackgroundColor", settings.call_tips_background_color)
        # self._set_color("setCallTipsForegroundColor", settings.call_tips_foreground_color)
        # self._set_color("setCallTipsHighlightColor", settings.call_tips_highlight_color)
        self._set_color("setCaretForegroundColor", settings.caret)
        # self._set_color("setCaretLineBackgroundColor", settings.caret_line_background_color)
        # self._set_color("setColor", settings.color)
        # self._set_color("setEdgeColor", settings.edge_color)
        # self._set_color("setFoldMarginColors", settings.fold_margin_colors)
        # self._set_color("setHotspotBackgroundColor", settings.hotspot_background_color)
        # self._set_color("setHotspotForegroundColor", settings.hotspot_foreground_color)
        self._set_color("setIndentationGuidesBackgroundColor", settings.guide)
        self._set_color("setIndentationGuidesForegroundColor", settings.guide)
        # self._set_color("setIndicatorForegroundColor", settings.indicator_foreground_color)
        # self._set_color("setIndicatorHoverForegroundColor", settings.indicator_hover_foreground_color)
        # self._set_color("setIndicatorOutlineColor", settings.indicator_outline_color)
        # self._set_color("setMarginBackgroundColor", settings.margin_background_color)
        # self._set_color("setMarginsBackgroundColor", settings.margins_background_color)
        # self._set_color("setMarginsForegroundColor", settings.margins_foreground_color)
        # self._set_color("setMarkerBackgroundColor", settings.marker_background_color)
        # self._set_color("setMarkerForegroundColor", settings.marker_foreground_color)
        self._set_color("setMatchedBraceBackgroundColor", settings.brackets_background)
        self._set_color("setMatchedBraceForegroundColor", settings.brackets_foreground)
        self._set_color("setSelectionBackgroundColor", settings.selection)
        # self._set_color("setSelectionBackgroundColor", settings.selection_background)
        # self._set_color("setSelectionForegroundColor", settings.selection_foreground)
        # self._set_color("setUnmatchedBraceBackgroundColor", settings.unmatched_brace_background_color)
        # self._set_color("setUnmatchedBraceForegroundColor", settings.unmatched_brace_foreground_color)
        # self._set_color("setWhitespaceBackgroundColor", settings.whitespace_background_color)
        # self._set_color("setWhitespaceForegroundColor", settings.whitespace_foreground_color)

        bc = settings.background
        self.resetFoldMarginColors()
        self.setFoldMarginColors(qt_color(bc), qt_color(bc))

        self.lexer = ViewLexer(self.ss, self.syntax, self.theme, parent=self)
        self.setLexer(self.lexer)
