# Worksets

Worksets helps you to quickly launch and arrange multiple applications in your desktop environment to support a specific workflow.
Built for Unity 7 (R.I.P) and has been tested on Ubuntu 16.04.

| <img src="/doc/images/tray_menu.png?raw=true" width="160"> | <img src="/doc/images/app_dialog.png?raw=true" width="260"> |
|:---:|:---:|
| Tray menu | Application dialog |


### Features

* Create worksets for running and placing apps in predefined positions on the monitor and desktop of your choice
* Define scripts to be run at start of workset launch
* Easy access to use, create and manage your worksets through the systemtray
* Open *and* close worksets from the systemtray (you *should* be prompted to save your work)

### Requirements
* Unity 7 with X11 window manager (Tested on Ubuntu 16.04)
* Python 3
* PyQt5
* TinyDB
* wmctrl
* xdotool

### License
Worksets is licensed under the GNU General Public License v3 or later.  

## Why?
Some workflows involves multiple "applications" and regularly switching between them.
Such a workflow could be something you do every day or something you need to work on for a limited time. 

With Worksets you can make this setup once and rely on the click of a button to set it up for you afterwards. This could all be done with bash, wmctrl and xdotool already, but you would have to fiddle around with x and y coordinates and sizes, full desktop area etc. which could be a cumbersome proces (especially if the hardware setup later changes) and as such would quickly eat up the benefits timewise of doing this.

## So..?

You will still have to configure the worksets manually, but the configuration has been made a gazillion times easier than doing it through bash scripts with wmctrl and xdotool.

What you need to do is:

* Specify the executable you want to launch
* Supply specific parameters for the executable (say if you want to open a website or a specific file)
* Choose between predefined placements on available monitors and desktops
* save and repeat until your workset is complete 

Available desktops and monitors are determined at launch.

**Please do understand that this is a learning/hobby project of mine and as such development can be slow. I do hope however that somebody will find it useful**

## How to install

*For now installation is only possible from source distribution file.*  

Step-by-step instructions for installation with pip can be found in the [wiki](https://github.com/DozyDolphin/Worksets/wiki/How-to-install%2C-run-or-uninstall-worksets)

## How to use worksets

Please see the instructions in the [wiki](https://github.com/DozyDolphin/Worksets/wiki/How-to-use-worksets)

# Development

TODO