import os
from posixpath import expanduser
import subprocess
from typing import List
from libqtile import bar, layout, widget, qtile
from libqtile import hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"

home = os.path.expanduser("~")

terminal = "alacritty"

# Start the selected apps when Qtile start
@hook.subscribe.startup_once
def autostart():
    qtile.spawn("dunst -conf ~/.config/dunst/qtilerc")
    qtile.spawn("nm-applet")

keys = [

    #Focus windows
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    #Cycle focus
    Key([mod], "space", lazy.layout.next()),

    #Move windows
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    #Grow windows
    Key([mod, "control"],
        "Left",
        # lazy.layout.grow_left(),
        # lazy.layout.shrink_left(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"],
        "Right",
        # lazy.layout.grow_right(),
        # lazy.layout.shrink_right(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"],
        "Down",
        # lazy.layout.grow(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"],
        "Up",
        lazy.layout.grow(),
        # lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"],
        "k",
        lazy.layout.grow_left()
        ),
    Key([mod, "control"],
        "l",
        lazy.layout.grow_right()
        ),
    Key([mod, "control"],
        "j",
        lazy.layout.grow_down()
        ),
    Key([mod, "control"],
        "k",
        lazy.layout.grow_up()
        ),

    #Reset layout
    Key([mod], "n", lazy.layout.normalize()),

    #Open Alacritty
    Key([mod], "Return", lazy.spawn(terminal)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),

    #kill the focused window
    Key([mod, "shift"], "q", lazy.window.kill()),

    #Fullscreen the focused window
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    #Togle whether floating or not the focused windows
    Key([mod], "t", lazy.window.toggle_floating()),

    #reload all Qtile using the config.py
    Key([mod, "shift"], "r", lazy.reload_config()),

    #Quit Qtile
    Key([mod, "control"], "q", lazy.shutdown()),

    #Open rofi
    Key(["mod1"], "Tab", lazy.spawn("rofi -show drun")),
]

# color arays
def init_colors():
    return [
        ["#1d2021", "#1d2021"],  # 0 background
        ["#fbf1c7", "#fbf1c7"],  # 1 foreground
        ["#3b4252", "#3b4252"],  # 2 background lighter
        ["#cc241d", "#cc241d"],  # 3 red
        ["#98971a", "#98971a"],  # 4 green
        ["#d79921", "#d79921"],  # 5 yellow
        ["#458588", "#458588"],  # 6 blue
        ["#b16286", "#b16286"],  # 7 magenta
        ["#689d6a", "#689d6a"],  # 8 cyan
        ["#d08770", "#d08770"],  # 9 orange
        ["#a89984", "#a89984"],  # 10 white
        ["#282828", "#282828"],  # 11 black
        ["#cc241d", "#cc241d"],  # 12 red lighter
        ["#98971a", "#98971a"],  # 13 green lighter
        ["#d79921", "#d79921"],  # 14 yellow lighter
        ["#458588", "#458588"],  # 15 blue lighter
        ["#b16286", "#b16286"],  # 16 magenta lighter
        ["#689d6a", "#689d6a"],  # 17 cyan lighter
        ["#ebdbb2", "#ebdbb2"],  # 18 white lighter
        ["#928374", "#928374"],  # 19 black lighter
    ]
colors = init_colors()

groups = [Group(i) for i in "1234"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),

            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
            ),
       ]
    )
    

layouts = [
    # layout.Tile(margin=8,
    #     border_focus=colors[1],
    #     border_normal=colors[0],
    #     border_width=4,),
    
    # layout.Bsp(
    #     margin=8,
    #     border_focus=colors[1],
    #     border_normal=colors[0],
    #     border_width=4,
    #     ),
    
    # layout.Columns(
    #     margin=8,
    #     border_focus=colors[1],
    #     border_normal=colors[0],
    #     border_width=4,
    #     ),
    
    layout.MonadTall(
        margin=8,
        border_focus=colors[1],
        border_normal=colors[0],
        border_width=4,
    ),
    
    layout.Max(
        margin=8,
        border_focus=colors[1],
        border_normal=colors[0],
        border_width=4,
        ),

    #layout.Stack(num_stacks=2),
    # layout.Matrix(),
    #layout.MonadWide(),
    # layout.RatioTile(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font="Cascadia Mono",
    fontsize=12,
    padding=0,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    # Resort Groups by draging them wiht the mouse, disabled by default
                    disable_drag=True,

                    # Text colors
                    block_highlight_text_color=colors[0],
                    inactive=colors[1],

                    # Highlight aspect
                    highlight_color=colors[1],
                    highlight_method="line",

                    # Border aspect
                    borderwidth=4,
                    this_current_screen_border=colors[1],

                    padding=10,
                    ),
                widget.WindowName(
                    markup=True,

                    foreground=colors[1],
                    
                    padding = 8
                    ),
                widget.CurrentLayout(
                    background=colors[3],
                    foreground=colors[1],

                    padding=6,
                    ),
                widget.Memory(
                    format = '{MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}',

                    measure_mem='M',

					background=colors[5],
                    foreground=colors[0],

                    padding=6
                    ),
                widget.Sep(
					background=colors[5],

                    linewidth=0,

                    padding=6,
                    ),
                widget.CPU(
                    format = 'CPU {load_percent}%',

					background=colors[4],
                    foreground=colors[0],

                    padding=8,
                    ),
                widget.Battery(
                    format = "BAT {percent:2.0%}",

                    background=colors[8],
                    foreground=colors[0],

                    update_interval = 5,

                    padding=8,
                    ),
                widget.TextBox(
                    format='',
                    foreground=colors[6],
                ),
                widget.Clock(
					format="%Y-%m-%d %H:%M",

					background=colors[6],
                    foreground=colors[0],

					padding=8,
					),
                widget.Systray(
                    padding=8,
                    ),
                widget.Sep(
                    linewidth=0,

                    padding=12,
                    ),
            ],
                size=32,

                background=colors[0],
                border_color=["#fbf1c7", "#fbf1c7", "#fbf1c7", "#fbf1c7"],

                border_width=[4, 4, 4, 4],

                margin=[0, 8, 8, 8],
                ),
        x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wl_input_rules = None

wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"
