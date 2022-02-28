import fire
from add_quiz import add_quiz
import pyautogui as gui
from time import sleep


class Cli(object):

    def add_quiz(self, csv_path):
        add_quiz(csv_path)
        return 'quiz added'

    def pos(self):
        while True:
            print(gui.position())
            sleep(1)
        return 'end'


if __name__ == '__main__':
    fire.Fire(Cli)
