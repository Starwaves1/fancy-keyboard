#!/bin/zsh
# Regenerates build/*.keylayout and the white menu-bar icons.
set -e
cd "${0:A:h}"
python3 gen.py build
swiftc -O tools/icon.swift -o tools/icon
for pair in "Script:𝓐" "Monospace:𝙰" "Fraktur:𝕬" "Double-Struck:𝔸"; do
  n=${pair%%:*}; g=${pair#*:}; d="build/$n.iconset"; mkdir -p "$d"
  for s in 16 32; do
    tools/icon "$g" "$d/icon_${s}x${s}.png" $s
    tools/icon "$g" "$d/icon_${s}x${s}@2x.png" $((s * 2))
  done
  iconutil -c icns "$d" -o "build/$n.icns" && rm -r "$d"
done
