# tpinchasi.github.io

The website of IFocus, an Android app: its home page, privacy policy and terms,
served by GitHub Pages at https://tpinchasi.github.io/.

- `index.html`: the home page, in English and Hebrew.
- `privacy.html` and `terms.html`: the privacy policy and the terms of
  service, made from the app's `PRIVACY.md` and `TERMS.md`:

      python3 tools/pages.py ../transcript/perfect-spouse

- `join/`: where an invitation to a sharing group leads, if IFocus doesn't
  open it; `.well-known/assetlinks.json` makes those links open in the app.
- `style.css`, `rubik.ttf` (the app's font, SIL Open Font License), the icons.

Nothing on the site loads from other servers.
