import os
from random import shuffle
from flask import Flask, session, request, redirect, render_template, url_for
from db_script import get_question_after, get_quises, check_answer

def start_quiz(quiz_id):
    '''создаёт нужные значения в словаре session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    ''' функция получает список викторин из базы и формирует форму с выпадающим списком'''
    q_list = get_quises()
    return render_template('start.html', q_list=q_list)


def index():
    ''' Первая страница: если пришли запросом GET, то выбрать викторину,
    если POST - то запомнить id викторины и отправлять на вопросы'''
    if request.method == 'GET':
        # викторина не выбрана, сбрасываем id викторины и показываем форму выбора
        start_quiz(-1)
        return quiz_form()
    else:
        # получили дополнительные данные в запросе! Используем их:
        quest_id = request.form.get('quiz') # выбранный номер викторины
        start_quiz(quest_id)
        return redirect(url_for('test'))

def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1

def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)

def test():
    if request.method == 'POST':
        save_answers()
    next_question = get_question_after(session['last_question'], session['quiz'])
    if next_question is None or len(next_question) == 0:
        return redirect(url_for('result'))
    else:
        return question_form(next_question)

def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html

folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == "__main__":
    app.run()