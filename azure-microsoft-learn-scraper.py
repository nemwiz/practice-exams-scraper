from bs4 import BeautifulSoup
from anki_card_creator import create_anki_card

with open('azure/azure-network-security.html') as file:
    soup = BeautifulSoup(file, 'html.parser')

    exam = []
    count = 0

    for index, question_container in enumerate(soup.find_all(attrs={'class': 'quiz-question'}), start=1):
        exam_question = dict()

        question = ' '.join(question_container.find(id='quiz-question-{}'.format(index)).p.text.split())

        exam_question.setdefault('question', question)
        exam_question.setdefault('question-type', 2)
        exam_question.setdefault('explanation', '')

        answers = []

        for answer_label in question_container.find_all('label'):
            answer = dict()
            answer.setdefault('is_correct', False)

            if answer_label.attrs.get('aria-label') and 'Correct answer' in answer_label.attrs['aria-label']:
                answer.update({'is_correct': True})

            answer_text = ' '.join(answer_label.div.p.text.split())
            answer.update({'answer': answer_text})
            answers.append(answer)

        exam_question.setdefault('answers', answers)

        answer_pattern = [int(answer.get('is_correct')) for answer in answers]
        answer_pattern_template = ' '.join(['{}' for i in range(len(answers))])
        exam_question.setdefault('anki-card-answer-pattern', answer_pattern_template.format(*answer_pattern))

        explanation_containers = question_container.find_all(class_='quiz-choice-explanation')

        for explanation_container in explanation_containers:
            if explanation_container.p and 'is-correct' in explanation_container.previous_sibling.previous_sibling.attrs['class']:

                explanation = ' '.join(explanation_container.p.text.split())
                if "That's correct" in explanation:
                    exam_question.update({'explanation': explanation.replace("That's correct. ", '')})

                exam_question.update({'explanation': explanation})

        print(exam_question)

        exam.append(exam_question)

    for exam_question in exam:
        create_anki_card(exam_question)
