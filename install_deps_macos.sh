#!/bin/bash
# needed in general
echo "Installing system dependencies"
brew install py3cairo ffmpeg

# only for apple sillicon machines
chip=$(uname -m | tail -n1)
if [[ "$chip" == "arm64" ]]; then
    echo "Installing apple silicon dependencies"
    brew install pango pkg-config scipy
fi

# optional dependencies
if [[ "$1" == "--optional"  ]] || [[ "$1" == "-o" ]]; then
    echo "Installing optional dependencies"
    brew install --cask mactex-no-gui
fi
