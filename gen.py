"""Generate macOS .keylayout files that type Unicode "fonts" (math alphanumerics).

Base/Shift/Caps produce the styled letters; Option produces plain ASCII
(escape hatch); Command and Control produce plain ASCII so shortcuts work.
"""
import sys
from pathlib import Path

US = {  # keycode: (unshifted, shifted)
    0: "aA", 1: "sS", 2: "dD", 3: "fF", 4: "hH", 5: "gG", 6: "zZ", 7: "xX", 8: "cC", 9: "vV",
    10: "§±", 11: "bB", 12: "qQ", 13: "wW", 14: "eE", 15: "rR", 16: "yY", 17: "tT",
    18: "1!", 19: "2@", 20: "3#", 21: "4$", 22: "6^", 23: "5%", 24: "=+", 25: "9(", 26: "7&",
    27: "-_", 28: "8*", 29: "0)", 30: "]}", 31: "oO", 32: "uU", 33: "[{", 34: "iI", 35: "pP",
    37: "lL", 38: "jJ", 39: "'\"", 40: "kK", 41: ";:", 42: "\\|", 43: ",<", 44: "/?", 45: "nN",
    46: "mM", 47: ".>", 50: "`~",
    65: "..", 67: "**", 69: "++", 75: "//", 78: "--", 81: "==",
    82: "00", 83: "11", 84: "22", 85: "33", 86: "44", 87: "55", 88: "66", 89: "77", 91: "88", 92: "99",
}
SPECIAL = {
    36: "\r", 48: "\t", 49: " ", 51: "\x08", 52: "\x03", 53: "\x1b", 71: "\x1b", 76: "\x03",
    114: "\x05", 115: "\x01", 116: "\x0b", 117: "\x7f", 119: "\x04", 121: "\x0c",
    123: "\x1c", 124: "\x1d", 125: "\x1f", 126: "\x1e",
    **{k: "\x10" for k in (96, 97, 98, 99, 100, 101, 103, 105, 106, 107, 109, 111, 113, 118, 120, 122)},
}


def alpha(upper, lower, holes=None, digits=None):
    holes = {**(holes or {}), **PUNCT.get(upper, {})}
    def f(c):
        if holes and c in holes:
            return holes[c]
        if "A" <= c <= "Z":
            return chr(upper + ord(c) - 65)
        if "a" <= c <= "z":
            return chr(lower + ord(c) - 97)
        if digits is not None and "0" <= c <= "9":
            return chr(digits + ord(c) - 48)
        return c
    return f


# Unicode has no styled punctuation; ornaments stand in where one renders on macOS/iOS.
PUNCT = {0x1D4D0: {"!": "❢"}, 0x1D56C: {"!": "❢"}}

STYLES = {
    "Script": (-29001, alpha(0x1D4D0, 0x1D4EA), "𝓐"),
    "Monospace": (-29002, alpha(0x1D670, 0x1D68A, digits=0x1D7F6), "𝙰"),
    "Fraktur": (-29003, alpha(0x1D56C, 0x1D586), "𝕬"),
    "Double-Struck": (-29004, alpha(0x1D538, 0x1D552, digits=0x1D7D8, holes={
        "C": "ℂ", "H": "ℍ", "N": "ℕ", "P": "ℙ", "Q": "ℚ", "R": "ℝ", "Z": "ℤ"}), "𝔸"),
}


def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if o < 0x20 or o == 0x7F or ch in "&<>\"'":
            out.append(f"&#x{o:04X};")
        else:
            out.append(ch)
    return "".join(out)


def keymap(index, out):
    lines = [f'\t\t<keyMap index="{index}">']
    for code in sorted({*US, *SPECIAL}):
        lines.append(f'\t\t\t<key code="{code}" output="{esc(out(code))}"/>')
    lines.append("\t\t</keyMap>")
    return "\n".join(lines)


def layout(name, kid, style):
    def plain(shift):
        return lambda k: SPECIAL[k] if k in SPECIAL else US[k][shift]

    def ctrl(k):
        if k in SPECIAL:
            return SPECIAL[k]
        c = US[k][0]
        if "a" <= c <= "z":
            return chr(ord(c) - 96)
        return {"[": "\x1b", "\\": "\x1c", "]": "\x1d", "6": "\x1e", "-": "\x1f"}.get(c, c)

    maps = [
        keymap(0, lambda k: SPECIAL.get(k) or style(US[k][0])),
        keymap(1, lambda k: SPECIAL.get(k) or style(US[k][1])),
        keymap(2, lambda k: "–" if k == 27 else plain(0)(k)),  # Option-hyphen: en dash, as on U.S.
        keymap(3, lambda k: "—" if k == 27 else plain(1)(k)),  # Option-Shift-hyphen: em dash
        keymap(4, plain(0)),
        keymap(5, ctrl),
    ]
    caps_upper = keymap(6, lambda k: SPECIAL.get(k) or style(US[k][1] if US[k][0].isalpha() else US[k][0]))
    return f"""<?xml version="1.1" encoding="UTF-8"?>
<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">
<keyboard group="126" id="{kid}" name="{name}" maxout="2">
\t<layouts>
\t\t<layout first="0" last="17" modifiers="mods" mapSet="maps"/>
\t</layouts>
\t<modifierMap id="mods" defaultIndex="0">
\t\t<keyMapSelect mapIndex="0"><modifier keys=""/></keyMapSelect>
\t\t<keyMapSelect mapIndex="1"><modifier keys="anyShift caps?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="6"><modifier keys="caps"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="2"><modifier keys="anyOption caps?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="3"><modifier keys="anyOption anyShift caps?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="4"><modifier keys="command anyShift? anyOption? caps? anyControl?"/></keyMapSelect>
\t\t<keyMapSelect mapIndex="5"><modifier keys="anyControl anyShift? anyOption? caps?"/></keyMapSelect>
\t</modifierMap>
\t<keyMapSet id="maps">
{chr(10).join(maps)}
{caps_upper}
\t</keyMapSet>
</keyboard>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, (kid, style, _) in STYLES.items():
        (out / f"{name}.keylayout").write_text(layout(name, kid, style), encoding="utf-8")
        print(name)
