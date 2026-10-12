#!/bin/zsh
# Installs the layouts for the current user and enables them in the input menu.
set -e
cd "${0:A:h}"
dest=~/Library/"Keyboard Layouts"
mkdir -p "$dest"
cp build/*.keylayout build/*.icns "$dest"/
# Must match the ids in gen.py. TISEnableInputSource reports success but doesn't
# enable unsigned layouts, so add them to the enabled list directly.
for p in "-29001:Script" "-29002:Monospace" "-29003:Fraktur" "-29004:Double-Struck"; do
  id=${p%%:*}; name=${p#*:}
  if ! defaults read com.apple.HIToolbox AppleEnabledInputSources 2>/dev/null | grep -qE "Name\" = \"?$name\"?;"; then
    defaults write com.apple.HIToolbox AppleEnabledInputSources -array-add \
      "<dict><key>InputSourceKind</key><string>Keyboard Layout</string><key>KeyboardLayout ID</key><integer>$id</integer><key>KeyboardLayout Name</key><string>$name</string></dict>"
  fi
done
killall TextInputMenuAgent 2>/dev/null || true
echo "Installed. If they don't show in the input menu, log out and back in."
