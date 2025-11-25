#! /bin/sh

xrdb -merge ~/.Xresources

if [ -f "${XDG_CONFIG_HOME:-$HOME/.config}/x11/xprofile" ]; then
	. "${XDG_CONFIG_HOME:-$HOME/.config}/x11/xprofile"
else
	. "$HOME/.xprofile"
fi

# exec xautolock -time 5 -locker slock &
# exec slstatus &
# exec dwm
exec qtile start
