import pyautogui
import pyperclip

pyautogui.PAUSE = 1
MULTIPLE_CHOICE_QUESTION = 1
SINGLE_CHOICE_QUESTION = 2
MAX_QUESTIONS = 5


def create_anki_card(exam_question):
    pyautogui.moveTo(2764, 266)
    pyperclip.copy(exam_question.get('question'))
    pyautogui.click()

    pyautogui.hotkey('ctrl', 'v')

    pyautogui.press('tab')
    pyautogui.press('tab')

    question_type = exam_question.get('question-type')
    pyperclip.copy(question_type)
    pyautogui.hotkey('ctrl', 'v')

    for answer in exam_question.get('answers'):
        pyautogui.press('tab')
        pyperclip.copy(answer.get('answer'))
        pyautogui.hotkey('ctrl', 'v')

    for i in range(MAX_QUESTIONS - len(exam_question.get('answers'))):
        pyautogui.press('tab')

    pyautogui.press('tab')

    pyperclip.copy(exam_question.get('anki-card-answer-pattern'))
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.press('tab')

    pyperclip.copy(exam_question.get('explanation'))
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.moveTo(3522, 783)
    pyautogui.click()
