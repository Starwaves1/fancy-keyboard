# 𝓯𝓪𝓷𝓬𝔂 𝓴𝓮𝔂𝓫𝓸𝓪𝓻𝓭

macOS keyboard layouts that type in Unicode "fonts". Pick one from the input menu and type normally:

| Layout | Types |
|---|---|
| Script | 𝓷𝓸𝓽𝓱𝓲𝓷𝓰. 𝓼𝓸𝓻𝓻𝔂 𝓽𝓸 𝓫𝓸𝓽𝓱𝓮𝓻. |
| Monospace | 𝚠𝚑𝚊𝚝 𝚊𝚋𝚘𝚞𝚝 𝚒𝚝 |
| Fraktur | 𝖋𝖗𝖆𝖓𝖐𝖋𝖚𝖗𝖙 |
| Double-Struck | 𝕨𝕒𝕙𝕡𝕠𝕨 |

These are Unicode characters (Mathematical Alphanumeric Symbols), not a font, so the style survives pasting into TikTok, Discord, iMessage, anywhere.

- Shift and Caps Lock give styled capitals. Monospace and Double-Struck have styled digits.
- ⌘ and ⌃ shortcuts type plain letters, so copy/paste and terminal Ctrl-C still work.
- ⌥ + key types the plain letter. ⌥- is an en dash (–), ⌥⇧- an em dash (—).
- Script and Fraktur turn `!` into `❢`. Unicode has no styled punctuation; see [docs/punctuation-options.png](docs/punctuation-options.png) for the other candidates and why they lost.

## Install

```sh
git clone https://github.com/Starwaves1/fancy-keyboard
cd fancy-keyboard
./install.sh
```

If the layouts don't appear in the input menu, log out and back in, or add them under Keyboard Settings → Input Sources → Edit → + → Others.

To uninstall, remove them in that same Settings pane and delete the `.keylayout` and `.icns` files from `~/Library/Keyboard Layouts`.

## Adding a style

Add an entry to `STYLES` in `gen.py` (the Unicode block's capital A, small a, and optionally digit 0 plus any reserved-slot substitutes), add its icon glyph and id to `build.sh` and `install.sh`, then run `./build.sh && ./install.sh`.

`tools/verify.swift` runs a sentence through each installed layout with `UCKeyTranslate`, which checks the compiled output without needing to type anything.

## Caveats

- Screen readers read these as math symbols ("mathematical bold script small n…"), and the text won't match normal searches.
- Changed icons are cached in `$(getconf DARWIN_USER_CACHE_DIR)com.apple.IntlDataCache.le*`. Move those aside and run `killall TextInputMenuAgent` to refresh.
- The menu-bar icons are white, so they suit a dark menu bar.
