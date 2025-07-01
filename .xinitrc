#! /bin/sh

xrdb -merge ~/.Xresources

xrandr --output LVDS-1 --brightness 0.8

if [ -f "${XDG_CONFIG_HOME:-$HOME/.config}/x11/xprofile" ]; then
	. "${XDG_CONFIG_HOME:-$HOME/.config}/x11/xprofile"
else
	. "$HOME/.xprofile"
fi

exec slstatus &
dbus-update-activation-environment --all
dbus-launch ssh-agent dwm
