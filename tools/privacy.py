"""Makes privacy.html from IFocus's PRIVACY.md (Hebrew, then "---", then English).

    python3 tools/privacy.py ../transcript/perfect-spouse/PRIVACY.md

Only what the policy uses: "#" and "##" headings, paragraphs, "- " lists
(an item goes on over lines indented by two spaces), **bold** and [links](url).
"""
import html
import re
import sys
from pathlib import Path

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IFocus Privacy Policy</title>
<meta name="description" content="How IFocus handles your data: everything is processed on your phone, and nothing is sent to us.">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">

<nav class="top">
  <a class="brand" href="./"><img src="icon.png" alt="">IFocus</a>
  <div class="langs"><a href="#en" lang="en">English</a><a href="#he" lang="he">עברית</a><a href="./">Home</a></div>
</nav>

<main class="policy">
<section class="lang" id="en" lang="en" dir="ltr">
{en}
</section>

<section class="lang" id="he" lang="he" dir="rtl">
{he}
</section>
</main>

<footer>
  <a href="./">IFocus</a> · <a href="mailto:tomer.pinchassi@gmail.com">tomer.pinchassi@gmail.com</a> · © 2026 IFocus
</footer>

</div>
</body>
</html>
"""


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', out)
    # A bare email address becomes a link.
    out = re.sub(r"(?<![\w.@/:])([\w.+-]+@[\w-]+\.[\w.]+\w)", r'<a href="mailto:\1">\1</a>', out)
    return out


def block(md: str) -> str:
    out: list[str] = []
    para: list[str] = []
    items: list[str] = []

    def flush() -> None:
        if para:
            text = " ".join(para)
            cls = ' class="updated"' if re.match(r"^(Updated|עודכן):", text) else ""
            out.append(f"<p{cls}>{inline(text)}</p>")
            para.clear()
        if items:
            out.append("<ul>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in items) + "\n</ul>")
            items.clear()

    for line in md.splitlines():
        if not line.strip():
            flush()
        elif line.startswith("## "):
            flush()
            out.append(f"<h2>{inline(line[3:].strip())}</h2>")
        elif line.startswith("# "):
            flush()
            out.append(f"<h1>{inline(line[2:].strip())}</h1>")
        elif line.startswith("- "):
            if para:
                # A paragraph that introduces a list ends where the list begins.
                text = " ".join(para)
                out.append(f"<p>{inline(text)}</p>")
                para.clear()
            items.append(line[2:].strip())
        elif items and line.startswith("  "):
            items[-1] += " " + line.strip()
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def main() -> None:
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    he, en = re.split(r"^---\s*$", source, maxsplit=1, flags=re.M)
    page = PAGE.replace("{en}", block(en.strip())).replace("{he}", block(he.strip()))
    target = Path(__file__).resolve().parent.parent / "privacy.html"
    target.write_text(page, encoding="utf-8")
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
