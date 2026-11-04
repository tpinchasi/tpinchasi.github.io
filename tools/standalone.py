"""Makes index.html, privacy.html and terms.html self-contained, for uploading
to a host of their own (the domain Google's review asks for): the stylesheet,
the Rubik font and the icons inside each page, and the terms' link to the
privacy policy relative.

    python3 tools/standalone.py <out-dir>
"""
import base64
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent


def b64(name):
    return base64.b64encode((SRC / name).read_bytes()).decode()


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    css = (SRC / "style.css").read_text(encoding="utf-8").replace(
        'url("rubik.ttf") format("truetype")', 'url("data:font/ttf;base64,%s") format("truetype")' % b64("rubik.ttf"))
    for page in ("index.html", "privacy.html", "terms.html"):
        s = (SRC / page).read_text(encoding="utf-8")
        assert s.count('<link rel="stylesheet" href="style.css">') == 1, page
        s = s.replace('<link rel="stylesheet" href="style.css">', "<style>\n" + css + "\n</style>")
        s = s.replace('src="icon.png"', 'src="data:image/png;base64,%s"' % b64("icon.png"))
        s = s.replace('href="favicon.png"', 'href="data:image/png;base64,%s"' % b64("favicon.png"))
        s = s.replace('href="apple-touch-icon.png"', 'href="data:image/png;base64,%s"' % b64("apple-touch-icon.png"))
        s = s.replace("https://tpinchasi.github.io/privacy.html", "privacy.html")
        (out / page).write_text(s, encoding="utf-8")
        print("wrote", out / page)


if __name__ == "__main__":
    main(sys.argv[1])
