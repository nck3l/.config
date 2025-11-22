#! /bin/sh

xrdb -merge ~/.Xresources

if [ -f "${XDG_CONFIG_HOME:-$HOME/.config}/x11/xprofile" ]; then
	. "${XDG_CONFIG_HOME:-$HOME/.config}/x11/xprofile"
else
	. "$HOME/.xprofile"
fi

# The first 2 calls help pipewire and bluetooth services from regularly throwing errors.
dbus-update-activation-environment --all
export $(dbus-launch)
# exec xautolock -time 5 -locker slock &
# exec slstatus &
# dbus-launch ssh-agent dwm
exec qtile start
