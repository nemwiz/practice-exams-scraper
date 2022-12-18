import textwrap
from bs4 import BeautifulSoup

from anki_card_creator import create_anki_card

with open('azure/az-900-prep-exams/practice-exam-1.html') as file:
    soup = BeautifulSoup(file, 'html.parser')

    exam = []
    count = 0

    for index, question_container in enumerate(soup.find_all(attrs={'class': 'panel panel-default'}), start=1):

        exam_question = dict()

        question = ' '.join(question_container.find(attrs={'class': 'panel-heading exam-header'}).div.text.split())

        exam_question.setdefault('question', question)
        exam_question.setdefault('question-type', 2)
        exam_question.setdefault('explanation', '')

        answers = []

        for answer_label in question_container.find(attrs={'class': 'ans'}).ul.find_all('li'):
            answer = dict()
            answer.setdefault('is_correct', False)

            if 'list-group-item-warning' in answer_label.attrs.get('class'):
                answer.update({'is_correct': True})

            answer_text = answer_label.find('label').text
            answer.update({'answer': answer_text})
            answers.append(answer)

        exam_question.setdefault('answers', answers)

        answer_pattern = [int(answer.get('is_correct')) for answer in answers]
        answer_pattern_template = ' '.join(['{}' for i in range(len(answers))])
        exam_question.setdefault('anki-card-answer-pattern', answer_pattern_template.format(*answer_pattern))

        explanation_containers = question_container.find(id='showAns').find(tabindex='0')
        explanation = ' '.join(explanation_containers.text.split())

        exam_question.update({'explanation': explanation})

        print(exam_question)

        exam.append(exam_question)

for exam_question in exam:
    create_anki_card(exam_question)
