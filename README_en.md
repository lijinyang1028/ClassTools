# Class Utility Chest

A simple desktop toolset for class daily use. Made with Python + Tkinter.

## Features

* Beautiful graphical clock

  * Many themes, 12/24 hour mode, always on top, fade-in animation.
* Luck test

  * Random score (1–100), funny comment, and a hidden "Lucky King" popup.
* Easy to add new tools

  * All tools start from the same panel. Add a new tool with one line in `main.py`.

## Quick Start

### Requirements

* Python 3.6 or newer
* Only standard libraries (tkinter, random, datetime, time)

### Run

```bash
git clone https://github.com/lijinyang1028/my\\\_own\\\_library.git
cd my\\\_own\\\_library
python "精美图形化时钟.py"
```

> If you see font errors, change font names like `'苹方\\\_XX'` to `'Microsoft YaHei'` or `'Arial'`.

### Shortcuts (in clock window)

|Key|Action|
|-|-|
|`ESC`|Exit|
|`Space`|Change theme|
|`F1`|12h / 24h mode|
|`F2`|Show / hide seconds|
|`F3`|Open luck test|

## Project Files

```
.
├── 精美图形化时钟.py      # Main file – clock + panel
├── main.py               # Panel that holds all tools
├── lucktest.py           # Luck test module
├── websearcher.py        # (not finished) web search
└── README.md
```

## How to Add a New Tool?

1. Import your module in `main.py`.
2. Inside `FunctionPanel.\_\_init\_\_`, call `self.register\_function("Button name", self.your\_method)`.
3. Write `self.your\_method` – usually open a new `Toplevel` window.

Example:

```python
def \_my\_new\_feature(self):
    import my\_module
    my\_module.show\_window(self.winfo\_toplevel())
```

## Notes

* Tkinter theme change does not refresh child widgets automatically. You can add `refresh\_theme(bg, fg)` in `FunctionPanel` if needed.
* Luck test Easter egg uses `Toplevel`. The code already checks for parent window to avoid errors.

## Future Ideas

* \[ ] Web search (class news)
* \[ ] Timetable reminder
* \[ ] Countdown (exam, graduation)
* \[ ] Random name picker

## Contribute

Classmates can send pull requests or suggest ideas.

## License

MIT License

