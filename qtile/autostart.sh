#!/bin/zsh

setxkbmap -layout us &
xinput --set-prop "TPPS/2 IBM TrackPoint" 354 0.7 &
xrandr --output LVDS-1 --gamma 0.9:1.0:1.0 &
picom -b
dunst -conf ~/.config/dunst/config &
feh --bg-fill --random ~/Pictures/Wallpapers/* &
