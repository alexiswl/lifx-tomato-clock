# LIFX Based Tomato Clock

Based off the following Python packages
[![Python package CI tomato-clock](https://github.com/coolcode/tomato-clock/workflows/Python%20package/badge.svg?branch=master)](https://github.com/coolcode/tomato-clock/actions)
[![PyPI version tomato-clock](https://badge.fury.io/py/tomato-clock.svg)](https://pypi.python.org/pypi/tomato-clock/)

LIFX Tomato Clock is a simple command line pomodoro app.

Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique

## Installation

```
$ git clone https://github.com/coolcode/tomato-clock.git
$ cd lifx-tomato-clock
$ python3 lifx-tomato.py 
```

### LIFX Access token
Please read this [authentication page first]('https://api.developer.lifx.com/docs/authentication')
Create the folder `~/.lifx`. Change the modifications to 700 so that no one else on your computer can read it.
Then add in a file named 'lifx.yaml' and update accordingly.

```
$ cat ~/.lifx/lifx.yaml
access-token: <insert access token here>
groups:
  <name of your work room>:
    id: <group id>
    name: <group name>

```

### Getting the credentials for the above yaml file:
Head to the [LIFX API ENDPOINTS PAGE](https://api.developer.lifx.com/docs/list-lights) and head down to 'Try It Out'.
Insert 'all' into the selector page and your access token into the key.


## Terminal Output
```
🍅 tomato 25 minutes. Ctrl+C to exit
 🍅🍅---------------------------------------------- [8%] 23:4 ⏰ 
```

## Light Output:

Focus mode: Light will turn white and 100% for 25 mins
Stretch mode: Light will turn red with 100% saturation for 5 mins

