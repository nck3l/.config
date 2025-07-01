typeset -U PATH path
path=("$HOME/.local/bin" "$HOME/Android" "$path[@]")

if [ -d "$HOME/adb-fastboot/platform-tools" ] ; then
 export PATH="$HOME/adb-fastboot/platform-tools:$PATH"
fi

export PATH
export SUDO_ASKPASS='/usr/lib/ssh/x11-ssh-askpass'
