import pyautogui as gui
import pyperclip
import csv
from time import sleep
import constants

# ADD_BUTTON_POS = [433, 928]
# Q_FIELD_POS = [120, 285]
# SUGGEST_POS = [120, 548]
# SAVE_BUTTON_POS = [120, 735]

SHORT_DELAY = 0.20

gui.PAUSE = SHORT_DELAY


def add_item(q, a):

    def confirm_ok():
        gui.keyDown('tab')
        gui.keyDown('tab')
        gui.keyDown('enter')

    # click add button
    gui.click(*constants.ADD_BUTTON_POS)
    gui.click(*constants.ADD_BUTTON_POS)

    # input qa
    gui.click(*constants.Q_FIELD_POS)
    pyperclip.copy(q)
    gui.hotkey('command', 'v')
    gui.keyDown('tab')
    pyperclip.copy(a)
    gui.hotkey('command', 'v')
    gui.keyDown('escape')
    sleep(SHORT_DELAY * 3)

    # suggest
    gui.scroll(-20)
    sleep(SHORT_DELAY * 2)
    gui.click(*constants.SUGGEST_POS)
    confirm_ok()
    sleep(SHORT_DELAY * 10)

    # save
    gui.click(*constants.SAVE_BUTTON_POS)
    sleep(SHORT_DELAY * 5)
    confirm_ok()

    return True


def add_quiz(csv_path):

    with open(csv_path, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        # 先頭の行はスキップ
        next(csvreader)
        l = list(filter(lambda r: not r[0], [row for row in csvreader]))
        lines_len = len(l)
        for i, row in enumerate(l):
            add_item(row[1], row[2])
            sleep(SHORT_DELAY * 5)
            print('{}/{} done'.format(i + 1, lines_len))

    print("done")
