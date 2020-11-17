from tkinter import Tk
import pyautogui
import keyboard

from urllib.request import urlopen
from bs4 import BeautifulSoup

from win32gui import GetWindowText, GetForegroundWindow
import subprocess
import getpass

import time

"""

Discord bot idea for Discord conversations.

"""


TARGET_M_POS = (2489, 1300)
INDICATOR = '!'
INTERVAL = 1


def get_msg():
    for _ in range(3):
        pyautogui.tripleClick(TARGET_M_POS[0], TARGET_M_POS[1])

    keyboard.press("CTRL")
    keyboard.press("c")
    keyboard.release("CTRL")

    return Tk().clipboard_get()


def send_msg(text):
    keyboard.send("ENTER")  # Select chat bar
    keyboard.send("BACKSPACE")  # Remove newline
    keyboard.write(text)  # Type
    keyboard.send("ENTER")  # Send


def _extract(tag) -> (int, int):
    # In the case of profiles of pro players, format is:
    # [<span class="Name"> OFFICIAL NAME </span> <span class="Name"> ACCOUNT NAME </span>]
    # So, to find the '>' for the ACCOUNT NAME, we reverse search, avoiding the '>' at the end by
    # avoiding the last 2 chars ([:-2] splice)
    idx1 = tag[:-2].rfind('>') + 1
    idx2 = tag.rfind('<')

    return idx1, idx2


def rank_cmd(user):
    try:
        http_response_obj = urlopen(f"https://na.op.gg/summoner/userName={user}")  # Get HTML object

        html_str = http_response_obj.read().decode("utf-8")  # Take HTML as string
        s = BeautifulSoup(html_str, "html.parser")  # Parse the string

        trueNameTag = str(s.find_all("span", {"class": "Name"}))  # Get correct capitalization
        rankTag = str(s.find_all("div", {"class": "TierRank"}))  # Find string content of <div class=TierRank ... </div> tag

        nameIdx1, nameIdx2 = _extract(trueNameTag)
        rankIdx1, rankIdx2 = _extract(rankTag)

        if rankTag[rankIdx1: rankIdx2] != '[':
            send_msg(f"{trueNameTag[nameIdx1: nameIdx2].strip()} is currently {rankTag[rankIdx1: rankIdx2].strip()}.")

    except AttributeError:
        print("error")


def process_msg(text):
    if text[0] == '!':
        print(f"COMMAND MESSAGE: {text}")
        if text[1:5] == "rank":
            rank_cmd(text[text.find(' ') + 1:])


def main():
    while 1:
        if GetWindowText(GetForegroundWindow())[-7:] == "Discord":
            time.sleep(INTERVAL)
            process_msg(get_msg())

        if keyboard.is_pressed("SPACE"):
            break


if __name__ == '__main__':
    subprocess.Popen(rf"C:\Users\{getpass.getuser()}\AppData\Local\Discord\Update.exe --processStart Discord.exe")
    time.sleep(5)
    main()
