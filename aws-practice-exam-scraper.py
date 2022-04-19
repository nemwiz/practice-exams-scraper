from bs4 import BeautifulSoup

from anki_card_creator import create_anki_card

MULTIPLE_CHOICE_QUESTION = 1

SINGLE_CHOICE_QUESTION = 2


def scrape():
    with open('practice-test-6.html') as file:
        soup = BeautifulSoup(file, 'html.parser')

        exam = []
        count = 0

        for question_container in soup.select('div[class*="detailed-result-panel--question-container"]'):
            exam_question = dict()

            question = get_question(question_container)
            exam_question.setdefault('question', question)

            answers = get_answers(question_container)
            exam_question.setdefault('answers', answers)

            answer_pattern = [int(answer.get('is_correct')) for answer in answers]

            is_multiple_choice = len(answer_pattern) != 4
            exam_question.setdefault('question-type',
                                     MULTIPLE_CHOICE_QUESTION if is_multiple_choice else SINGLE_CHOICE_QUESTION)

            pattern = '{} {} {} {} {}' if is_multiple_choice else '{} {} {} {}'
            exam_question.setdefault('anki-card-answer-pattern', pattern.format(*answer_pattern))

            explanation = get_explanation(question_container)
            explanation = format_explanation(explanation, answers)

            exam_question.setdefault('explanation', explanation)

            exam.append(exam_question)

            print(exam_question)
        for exam_question in exam:
            create_anki_card(exam_question)
        return

        # for index, q in enumerate(exam, start=1):
        #
        #     print('---------------', index, '-----------------', '\n')
        #     print(q.get('question'), '\n')
        #
        #     for a in q.get('answers'):
        #         print(a, '\n')
        #
        #     print(q.get('anki-card-answer-pattern'))
        #     print(q.get('question-type'))
        #
        #     print(q.get('explanation'))
        #
        #     print('---------------', index, '-----------------', '\n')
        #     print('\n')


def format_explanation(explanation: str, answers: list) -> str:
    for answer in answers:
        start_index = explanation.find(answer.get('answer').strip())
        split_index = start_index + len(answer.get('answer').strip())

        explanation = explanation[:start_index] + '\n\n' + explanation[start_index:split_index] + '\n\n' + explanation[
                                                                                                           split_index:]

    return explanation


def get_explanation(question_container) -> str:
    for explanation in question_container.select('div[class*="mc-quiz-question--explanation"]'):
        explanation_text = ''

        for paragraph in explanation.find_all('p'):
            if paragraph.text.find('Correct option') != -1:
                explanation_text = explanation_text + paragraph.text.replace('\n', '')
                explanation_text = explanation_text + '\n\n'
                continue

            if paragraph.text.find('Incorrect options') != -1:
                explanation_text = explanation_text + '\n\n'
                explanation_text = explanation_text + paragraph.text.replace('\n', '')
                explanation_text = explanation_text + '\n\n'
                continue

            explanation_text = explanation_text + paragraph.text.replace('\n', '')

        return explanation_text


def get_answers(question_container) -> list:
    answers = []
    for index, answer_container in enumerate(
            question_container.select('div[class*="mc-quiz-answer--answer-body"]'), start=1):

        answer = dict()

        for answer_class in answer_container.attrs.get('class'):
            answer.setdefault('is_correct', False)
            if answer_class.find('--correct') != -1:
                answer.update({'is_correct': True})

        answer_text = ''
        for paragraph in answer_container.find_all('p'):
            answer_text = answer_text + paragraph.text + ' '

        answer.setdefault('answer', answer_text.replace('\n', ''))

        answers.append(answer)

    return answers


def get_question(question_container) -> str:
    for question in question_container.find_all(id='question-prompt'):
        questions_text = ''

        for paragraph in question.find_all('p'):
            questions_text = questions_text + paragraph.text.replace('\n', ' ')

        return questions_text.replace('\n', '')


if __name__ == '__main__':
    scrape()
