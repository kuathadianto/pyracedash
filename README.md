# pyracedash: Python Racing Dashboard
__pyracedash__ is an application for [Project CARS](http://store.steampowered.com/app/234630/Project_CARS/) and [Project CARS 2](http://store.steampowered.com/app/378860/Project_CARS_2/) which displays __in-game informations__ like RPM and speed. This application is intended to run on a [Raspberry Pi](https://www.raspberrypi.org/) with an LCD display and act as traditional [car dashboard](https://en.wikipedia.org/wiki/Dashboard). Although it is intended to run on a Raspberry Pi, it is not restricted to use this application on a standard PC/laptop running Windows, Mac OSX or Linux. __pyracedash__ is completely written in [Python](https://www.python.org/).

## Demo
__Note: Click image to see the video!__

[![pyracedashdemo1](http://img.youtube.com/vi/dBqbHMIZYLk/0.jpg)](https://www.youtube.com/watch?v=dBqbHMIZYLk)

[![pyracedashdemo2](http://img.youtube.com/vi/ohn47yIm4SM/0.jpg)](https://www.youtube.com/watch?v=ohn47yIm4SM)

[![pyracedashdemo3](http://img.youtube.com/vi/8caDRBJMeWU/0.jpg)](https://www.youtube.com/watch?v=8caDRBJMeWU)

_TODO: Add complete tutorial how to build video!_

## Prerequisites
[Project CARS REST API or CREST for short](https://cars-rest-api.com/) (ver. 1.0.2) should be running on host computer (the computer that runs the game) before the game is started, so that __pyracedash__ can get informations from the host computer. To do this, you can simply download the REST API [here](https://cars-rest-api.com/files/CREST-1.0.2.zip), unzip it, then run __CREST-1.0.2.exe__ before starting the game.

The host computer and the computer that runs __pyracedash__ should be connected via network (LAN cable, or WiFi, direct connection or through router).

## Installation
### Install on a Raspberry Pi
_TODO_
### Running on a PC/laptop
1. Install Python. You can download it [here](https://www.python.org/). Check "Add Python to PATH" on installation. Reboot after install. ![Add PATH on installation](https://loadbalancerblog.com/sites/default/files/images/image003.jpg)
2. Download [__pyracedash__](https://github.com/kuathadianto/pyracedash/archive/master.zip), unzip it.
3. Open Terminal/Command Prompt, change directory to the unzipped __pyracedash__ folder.
4. Run this command: `pip install -r requirements.txt`
5. Configure __pyracedash__ (see Configuration section).
6. Run it (double-click __pyracedash.py__)!

## Configuration
To configure __pyracedash__, you can open and edit __conf.ini__ located along with __pyracedash.py__. This is the sample of __conf.ini__:
```ini
[global]
X_RES = 800
Y_RES = 480
TITLE = "Kuat Hadianto's pyracedash"
FPS = 60
FULLSCREEN = 0
THEME = Fallback

[host]
IP_ADDRESS = 127.0.0.1
PORT = 8080
```
* __X_RES__: Length screen resolution.
* __Y_RES__: Width screen resolution.
* __TITLE__: Application Title.
* __FPS__: Frames Per Second. More FPS make it more responsive, but also make CPU works harder.
* __FULLSCREEN__: __1__ to enable it, __0__ to disable.
* __THEME__: Theme name that want to use. Default is Fallback. If theme is not found, it will choose Fallback. More themes comes later.
* __IP_ADDRESS__: IP address of host computer (computer that runs the game).
* __PORT__: Port which CREST use. DO NOT CHANGE IT!

## Help
For more info, questions, suggestions or feature requests, please contact me via twitter at: [@kuathadianto](https://twitter.com/kuathadianto)

Enjoy! :smile:
