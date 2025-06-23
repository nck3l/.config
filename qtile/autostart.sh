#!/bin/zsh

setxkbmap us &
xinput --set-prop "TPPS/2 IBM TrackPoint" 354 0.7 &
xrandr --output LVDS-1 --mode 1366x768 &
picom --backend glx &
dunst -conf ~/.config/dunst/config &
feh --bg-fill --random ~/Pictures/Wallpapers/* &
