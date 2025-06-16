# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy

# Definitions
mod = "mod4"            	# Sets mod key to SUPER/WINDOWS
mod1 = "control"			# Shortcut for the control key
myTerm = "kitty"      		# My terminal of choice
myAltTerm = "st"			# Alternate terminal
myBrowser = "brave"     	# My browser of choice
myEditor = "nvim" 			# My editor of choice
myOffice = "libreoffice"	# My office suite of choice
myFiles = "thunar"			# My GUI File Manager of choice
myIDE = "geany"				# My GUI editor of choice
myCalc = "qualculate"		# My calculator of choice
dmenufont = "Ubuntu Mono:size=10"

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'monadtall':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'monadtall'

keys = [
    # Program/Functions launchers
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "r", lazy.spawn("dmenu_run -m 0 -fn dmenufont -nb #222222 -nf #bbbbbb -sb #eeeeee -sf #444444"), desc='Run Launcher'),
    Key([mod], "w", lazy.spawn(myBrowser), desc='Web browser'),
    Key([mod], "t", lazy.spawn(myFiles), desc='File Manager'),
	Key([mod], "g", lazy.spawn(myIDE), desc='Geany Editor'),
    Key([mod], "c", lazy.spawn(myCalc), desc='Qualculate'),
    Key([mod], "o", lazy.spawn(myOffice), desc='LibreOffice'),
    Key([mod], "v", lazy.spawn("vlc"), desc='VLC Media Player'),
    Key([mod, mod1], "v", lazy.spawn("zathura ~/help/VimShortcuts.pdf"), desc='Vim Shortcuts'),
    Key([mod], "x", lazy.spawn("slock"), desc='Suckless Screen Locker'),
    Key([],	"Print", lazy.spawn("maim -i $(xdotool getactivewindow) ~/Pictures/Screenshots/window-$(date '+%y%m%d-%H%M-%S').png"), desc='Screenshot Active Window'),
    Key(["shift"], "Print", lazy.spawn("maim ~/Pictures/Screenshots/screen-$(date '+%y%m%d-%H%M-%S').png"), desc='Screenshot Screen'),
    Key([mod1], "Print", lazy.spawn("ffmpeg -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:2 -frames 1 ~/Pictures/Screenshots/out.jpg"), desc='Camera Selfie'),
    Key([], "XF86Launch1", lazy.spawn("zathura ~/help/KeyBindings.pdf"), desc='Key Bindings Cheatsheet'),

    # Basic Operations
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Quit Qtile"),

    # Volume keys
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%+")),

    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Grow/shrink windows left/right.
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", maximize_by_switching_layout(), lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7"]

# Uncomment only one of the following lines
group_labels = ["", "", "", "", "", "", ""]
#group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
#group_labels = ["", "WWW", "👁", "DOC", "", "", "MUS", "✀", "GFX", "⎙"]

# The default layout for each of the 7 workspaces
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

#for i in range(len(group_names)):
#    groups.append(
#        Group(
#            name=group_names[i],
#            layout=group_layouts[i].lower(),
#            label=group_labels[i],
#        ))

for i in "1234567":
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )
    
def Nord_colors():
	return [
    ["#2E3440", "#2E3440"], # color[0]
    ["#D8DEE9", "#D8DEE9"], # color[1]
    ["#3B4252", "#3B4252"], # color[2]
    ["#BF616A", "#BF616A"], # color[3]
    ["#A3BE8C", "#A3BE8C"], # color[4]
    ["#EBCB8B", "#EBCB8B"], # color[5]
    ["#81A1C1", "#81A1C1"], # color[6]
    ["#B48EAD", "#B48EAD"], # color[7]
    ["#88C0D0", "#88C0D0"], # color[8]
    ["#7d7d7d", "#7d7d7d"]  # color[9]
    ]
colors = Nord_colors()

layout_theme = {"border_width": 2,
                "margin": 12,
                "border_focus": colors[8],
                "border_normal": colors[0]
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),
    layout.Max(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme)
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Stack(**layout_theme, num_stacks=2),
    #layout.Columns(**layout_theme),
    #layout.TreeTab(
    #     font = "Ubuntu Bold",
    #     fontsize = 11,
    #     border_width = 0,
    #     bg_color = colors[0],
    #     active_bg = colors[8],
    #     active_fg = colors[2],
    #     inactive_bg = colors[1],
    #     inactive_fg = colors[0],
    #     padding_left = 8,
    #     padding_x = 8,
    #     padding_y = 6,
    #     sections = ["ONE", "TWO", "THREE"],
    #     section_fontsize = 10,
    #     section_fg = colors[7],
    #     section_top = 15,
    #     section_bottom = 15,
    #     level_shift = 8,
    #     vspace = 3,
    #     panel_width = 240
    #     ),
    #layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 12,
    padding = 0,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()
screens = [
	Screen(
		top = bar.Bar(
            [
			widget.Spacer(length = 8),
			widget.Image(
                 filename = "~/.config/qtile/icons/dt-icon.png",
                 scale = "False",
#                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("qtilekeys-yad")},
                 ),
			widget.Prompt(
                 font = "Ubuntu Mono",
                 fontsize=14,
                 foreground = colors[1]
				 ),
			widget.GroupBox(
                 fontsize = 11,
                 margin_y = 5,
                 margin_x = 14,
                 padding_y = 0,
                 padding_x = 2,
                 borderwidth = 3,
                 active = colors[8],
                 inactive = colors[9],
                 rounded = False,
                 highlight_color = colors[0],
                 highlight_method = "line",
                 this_current_screen_border = colors[7],
                 this_screen_border = colors [4],
                 other_current_screen_border = colors[7],
                 other_screen_border = colors[4],
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[9],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.LaunchBar(
                 progs = [("🦁", "brave", "Brave web browser"),
                          ("🚀", "kitty", "Kitty terminal"),
                          ("📁", "Thunar", "Thunar file manager"),
                          ("🎸", "vlc", "VLC media player")
                         ],
                 fontsize = 12,
                 padding = 12,
                 foreground = colors[3],
                ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[9],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.CurrentLayout(
                 foreground = colors[1],
                 padding = 5
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[9],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.WindowName(
                 foreground = colors[6],
                 padding = 8,
                 max_chars = 40
                 ),
        widget.GenPollText(
                 update_interval = 300,
                 func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 foreground = colors[3],
                 padding = 8,
                 fmt = '❤  {}',
                 ),
        widget.CPU(
                 foreground = colors[4],
                 padding = 8,
#                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                 format = ' Cpu: {load_percent}%',
                 ),
        widget.Memory(
                 foreground = colors[8],
                 padding = 8,
#                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                 format = '{MemUsed: .0f}{mm}',
                 fmt = ' Mem: {}',
                 ),
        widget.DF(
                 update_interval = 60,
                 foreground = colors[5],
                 padding = 8,
#                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-disk')},
                 partition = '/',
                 #format = '[{p}] {uf}{m} ({r:.0f}%)',
                 format = '{uf}{m} free',
                 fmt = '🖴  Disk: {}',
                 visible_on_warn = False,
                 ),
        widget.Volume(
                 foreground = colors[7],
                 padding = 8,
                 fmt = '  Vol: {}',
                 ),
        widget.Clock(
                 foreground = colors[8],
                 padding = 8,
#                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('notify-date')},
                 ## Uncomment for date and time
                 format = "%a, %e %B %y  %I:%M %p",
                 ## Uncomment for time only
                 # format = " %I:%M %p",
                 ),
        widget.Spacer(length = 8),
        ],
		24),
	),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    # Drag(["mod1"], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    # Drag(["mod1"], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    # Click(["mod1"], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
  #  subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
