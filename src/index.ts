import robot from "robotjs";
import fs from "fs";
import { parse } from "csv-parse/sync";

const { execSync } = require("child_process");
const MOUSE_POS_MODE = false;

type QA = {
  question: string;
  answer: string;
};

type Position = [number, number];

const ADD_BUTTON_POS: Position = [452, 922];
const QUESTION_FIELD_POS: Position = [228, 286];
const AUTO_FILL_BUTTON_POS: Position = [128, 590];
const SAVE_BUTTON_POS: Position = [123, 792];

const DELAY_SHORT = 200;
const DELAY_LONG = 900;

robot.setMouseDelay(60);
robot.setKeyboardDelay(80);

const delay = (t: number) => new Promise((res) => setTimeout(res, t));
const clipboardCopySync = (text: string) => {
  execSync("pbcopy", { input: text });
};

const addItem = async (qa: QA) => {
  // add
  const steps = [
    // add button
    async () => {
      robot.moveMouse(...ADD_BUTTON_POS);
      robot.mouseClick();
      robot.mouseClick();
    },

    // question
    () => {
      robot.moveMouse(...QUESTION_FIELD_POS);
      robot.mouseClick();
    },
    () => {
      clipboardCopySync(qa.question);
      robot.keyTap("v", "command");
    },

    // answer
    () => {
      clipboardCopySync(qa.answer);
      robot.keyTap("tab");
      robot.keyTap("v", "command");
      robot.keyTap("escape");
    },
    () => delay(DELAY_SHORT),

    // fill choices
    () => robot.scrollMouse(0, 9999),
    () => delay(DELAY_SHORT),
    () => {
      robot.moveMouse(...AUTO_FILL_BUTTON_POS);
      robot.mouseClick();
    },
    () => {
      // confirm
      robot.keyTap("tab");
      robot.keyTap("tab");
      robot.keyTap("enter");
    },
    () => delay(DELAY_SHORT),

    // save
    () => {
      robot.moveMouse(...SAVE_BUTTON_POS);
      robot.mouseClick();
    },
    () => delay(DELAY_SHORT),
    () => {
      // confirm
      robot.keyTap("tab");
      robot.keyTap("tab");
      robot.keyTap("enter");
    },
  ];
  for (const step of steps) {
    await step();
    await delay(DELAY_SHORT);
  }
};

const getQAList = async (): Promise<QA[]> => {
  const data = fs.readFileSync("./tmp/data.csv");
  const records = parse(data);
  return records
    .slice(1)
    .filter(([b]: string[]) => b === "")
    .map(
      ([_, question, answer]: string[]): QA => ({
        question,
        answer,
      })
    )
    .filter((qa: QA) => qa.question && qa.answer);
};

(async () => {
  if (MOUSE_POS_MODE) {
    while (1) {
      console.log(robot.getMousePos());
      await delay(DELAY_SHORT);
    }
  }
  const qaList = await getQAList();
  for (let i = 0; i < qaList.length; i++) {
    const qa = qaList[i];
    const numStr = `${i + 1} / ${qaList.length}`;
    console.log(`start: ${numStr}`);
    await addItem(qa);
    console.log(`done: ${numStr}`);
    await delay(DELAY_LONG);
  }
})();
