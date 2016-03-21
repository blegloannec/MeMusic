#!/bin/zsh

memusic="/home/bastien/SpiderOak\ Hive/memusic/memusic.py"
xterm -T memusic -e "$memusic $@; echo '[press enter to exit]'; read"
