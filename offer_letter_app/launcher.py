import sys
from pathlib import Path

from streamlit.web import bootstrap


def main() -> None:
    if getattr(sys, 'frozen', False):
        script_path = Path(sys._MEIPASS) / 'app.py'
    else:
        script_path = Path(__file__).resolve().parent / 'app.py'

    bootstrap.run(
        str(script_path),
        False,
        [],
        {},
    )


if __name__ == '__main__':
    main()
