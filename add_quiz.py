import pyautogui as gui
import pyperclip
import csv
from time import sleep

SHORT_DELAY = 0.20

gui.PAUSE = SHORT_DELAY


class AddQuiz():
    ADD_BTN_POS = None
    Q_FIELD_POS = None
    SUGGEST_BTN_POS = None
    SAVE_BTN_POS = None

    def add_quiz(self, csv_path):
        with open(csv_path, encoding='utf8', newline='') as f:
            csvreader = csv.reader(f)
            # 先頭の行はスキップ
            next(csvreader)
            l = list(filter(lambda r: not r[0], [row for row in csvreader]))
            lines_len = len(l)
            for i, row in enumerate(l):
                self.add_item(row[1], row[2])
                sleep(SHORT_DELAY * 5)
                print('{}/{} done'.format(i + 1, lines_len))
        print("done")

    def add_item(self, q, a):
        if not self.ADD_BTN_POS:
            self.ADD_BTN_POS = self.get_img_pos('add_button.png')

        def confirm_ok():
            gui.keyDown('tab')
            gui.keyDown('tab')
            gui.keyDown('enter')

        # click add button
        gui.click(*self.ADD_BTN_POS)
        sleep(SHORT_DELAY)
        gui.click(*self.ADD_BTN_POS)

        # input qa
        sleep(SHORT_DELAY * 2)
        if not self.Q_FIELD_POS:
            self.Q_FIELD_POS = self.get_img_pos('question_field.png')
        gui.click(*self.Q_FIELD_POS)
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

        if not self.SUGGEST_BTN_POS:
            self.SUGGEST_BTN_POS = self.get_img_pos('suggest_button.png')
        gui.click(*self.SUGGEST_BTN_POS)
        confirm_ok()
        sleep(SHORT_DELAY * 5)

        # save
        if not self.SAVE_BTN_POS:
            self.SAVE_BTN_POS = self.get_img_pos('save_button.png')
        gui.click(*self.SAVE_BTN_POS)
        sleep(SHORT_DELAY * 5)
        confirm_ok()

        return True

    def get_img_pos(self, fname):
        PIXEL_RATIO = 2
        POS_X, POS_Y = gui.locateCenterOnScreen(
            'ui_images/{}'.format(fname), confidence=0.8)
        return [POS_X / PIXEL_RATIO, POS_Y / PIXEL_RATIO]
