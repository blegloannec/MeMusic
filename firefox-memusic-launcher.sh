#!/bin/zsh

memusic="/path/to/memusic/memusic.py"
xterm -T memusic -e "$memusic $@; echo '[press enter to exit]'; read"
