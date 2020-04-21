#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import sys
import time
import subprocess

import requests
from pathlib import Path
import yaml
import time

# Set globals
LIFX_YAML_FILEPATH = Path.home() / ".lifx" / "lifx.yaml"
GROUP = "bedroom"
INITIAL_STATE_URL = "https://api.lifx.com/v1/lights/{0[selector]}/state"
CYCLE_STATE_URL = "https://api.lifx.com/v1/lights/{0[selector]}/cycle"

# Set states
STATES = {
    "Working":
        {
            "power": "on",
            "color": "white",
            "brightness": 1.0,
            "duration": 5
        },
    "Relaxing":
        {
            "power": "on",
            "color": "red saturation:1.0",
            "brightness": 1.0,
            "duration": 5
        }
}

WORK_MINUTES = 25
BREAK_MINUTES = 5

TOMATO_UNICODE = u"\U0001F345"
BATH_UNICODE = u"\U0001F6C0"
GOODBYE_UNICODE = u"\U0001F44B"
ALARM_CLOCK_UNICODE = u"\u23F0"


def read_lifx_yaml_file():
    # Open yaml file
    if not LIFX_YAML_FILEPATH.is_file():
        print("Error, couldn't open file {}, are you sure it exists".format(LIFX_YAML_FILEPATH))

    # Read with yaml
    with open(LIFX_YAML_FILEPATH, 'r') as access_token_fh:
        yaml_dict = yaml.load(access_token_fh)

    return yaml_dict


def get_access_token(yaml_dict):
    """
    Access token should be found in ~/.lifx/access-token.yaml
    :return:
    """

    # Check key exists
    if 'access-token' not in yaml_dict.keys():
        print("Error, could not find key 'access-token' in {}.".format(LIFX_YAML_FILEPATH))

    # Return value
    return yaml_dict['access-token']


def get_header(yaml_dict):
    """
    Header merely comprises the access token
    :return:
    """

    headers = {"Authorization": "Bearer {}".format(get_access_token(yaml_dict)),
               "Content-Type": "application/json"}

    return headers


def get_group(yaml_dict):
    """
    Return the attributes of the light group
    :param yaml_dict:
    :return:
    """

    group_dict = yaml_dict["groups"][GROUP]

    # Check group_dict has an id attribute
    if 'id' not in group_dict.keys():
        print("Error, expected to find an 'id' attribute in the group object")

    return group_dict


def get_init_state_url(group_dict):
    """
    Create the url for the put command
    Use the group ID for this component
    :param group_dict:
    :return:
    """

    # Get the group _id
    group_id = group_dict['id']
    selector = "group_id:{}".format(group_id)

    # Place this as the selector in the state url
    put_url = INITIAL_STATE_URL.format({"selector": selector})

    # Return the put url
    return put_url


def set_initial_state(group_dict, yaml_dict):
    """
    Set initial state to white
    :return:
    """
    # Request vars
    headers = get_header(yaml_dict)
    put_url = get_init_state_url(group_dict)
    json_body = STATES["Working"]

    # Request obj
    r = requests.put(put_url, headers=headers, json=json_body)

    json_response = r.json()
    print(json_response)


def get_cycle_state_url(group_dict):
    """
    Create the url for the put command
    Use the group ID for this component
    :param group_dict:
    :return:
    """

    # Get the group _id
    group_id = group_dict['id']
    selector = "group_id:{}".format(group_id)

    # Place this as the selector in the state url
    post_url = CYCLE_STATE_URL.format({"selector": selector})

    # Return the put url
    return post_url


def change_state(group_dict, yaml_dict):
    """
    Set initial state to white
    :return:
    """
    # Request vars
    headers = get_header(yaml_dict)
    post_url = get_cycle_state_url(group_dict)

    json_body = {"states": [STATES["Working"], STATES["Relaxing"]],
                 "defaults": STATES["Working"]}

    # Request obj
    r = requests.post(post_url, headers=headers, json=json_body)

    json_response = r.json()
    print(json_response)


def main():
    # Read in vars
    yaml_dict = read_lifx_yaml_file()

    # Get group dict
    group_dict = get_group(yaml_dict)

    # Set light to main light
    set_initial_state(group_dict, yaml_dict)

    try:
        if len(sys.argv) <= 1:
            print(f'{TOMATO_UNICODE} tomato {WORK_MINUTES} minutes. Ctrl+C to exit')
            tomato(WORK_MINUTES, 'It is time to take a break')
            change_state(group_dict, yaml_dict)

            print(f'{TOMATO_UNICODE} break {BREAK_MINUTES} minutes. Ctrl+C to exit')
            tomato(BREAK_MINUTES, 'It is time to work')
            change_state(group_dict, yaml_dict)

        elif sys.argv[1] == '-t':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            print(f'{BATH_UNICODE} tomato {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to take a break')
            change_state(group_dict, yaml_dict)

        elif sys.argv[1] == '-b':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            change_state(group_dict, yaml_dict)
            print(f'{BATH_UNICODE} break {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to work')
            change_state(group_dict, yaml_dict)

        elif sys.argv[1] == '-h':
            help()

        else:
            help()

    except KeyboardInterrupt:
        print(f"\n{GOODBYE_UNICODE} goodbye")
    except Exception as ex:
        print(ex)
        exit(1)


def tomato(minutes, notify_msg):
    start_time = time.perf_counter()

    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = '{}:{} {}'.format(int(left_seconds / 60), int(left_seconds % 60), ALARM_CLOCK_UNICODE)
        duration = min(minutes, 25)
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)

    notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', f'{TOMATO_UNICODE}' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def notify_me(msg):
    """
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    """

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(['terminal-notifier', '-title', f"{TOMATO_UNICODE}", '-message', msg])
            subprocess.run(['say', '-v', 'Daniel', msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", f"{TOMATO_UNICODE}", msg])
        else:
            # windows?
            # TODO: windows notification
            pass
    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== 🍅 Tomato Clock =======')
    print(f'{appname}         # start a {WORK_MINUTES} minutes tomato clock + {BREAK_MINUTES} minutes break')
    print(f'{appname} -t      # start a {WORK_MINUTES} minutes tomato clock')
    print(f'{appname} -t <n>  # start a <n> minutes tomato clock')
    print(f'{appname} -b      # take a {BREAK_MINUTES} minutes break')
    print(f'{appname} -b <n>  # take a <n> minutes break')
    print(f'{appname} -h      # help')


if __name__ == "__main__":
    main()
