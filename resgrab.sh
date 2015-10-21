#!/bin/bash
xrandr | grep [0-9]x[0-9] | cut -d ' '  -f 4 | sed 1d > res.txt
