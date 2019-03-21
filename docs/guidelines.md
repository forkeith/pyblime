# Guidelines

- The public interface of pyblime should remain as closely as possible to [View](https://www.sublimetext.com/docs/3/api_reference.html#sublime.View)
- A pyblime View by default should provide the SublimeText View functionality without any
external user plugin, so users should be able to register their own commands but
those commands won't be living in this repo
- SublimeText is the target and the widget should behave almost identically as
SublimeText (if possible because QScintilla limitations)

This project is not intended to become a SublimeText clone!!! Just a modern
standalone text editor widget that users will be able to customize like they
want to fit their needs.
