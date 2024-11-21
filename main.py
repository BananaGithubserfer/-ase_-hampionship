from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Для работы сессий

# Пример вопросов с вариантами ответов
questions = {
    "Какой цвет неба днём?": {
        "options": ["голубой", "зеленый", "красный", "черный"],
        "correct_answer": "голубой"
    },
    "Сколько дней в неделе?": {
        "options": ["шесть", "семь", "восемь", "пять"],
        "correct_answer": "семь"
    },
    "Столица Франции?": {
        "options": ["Берлин", "Лондон", "Париж", "Мадрид"],
        "correct_answer": "Париж"
    },
}

@app.route("/", methods=['GET'])
def index():
    # Сбрасываем сессию при входе на главную страницу
    session.clear()
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Инициализация сессии
    if "answers" not in session:
        session["answers"] = {}
    if "coins" not in session:
        session["coins"] = 0
    
    if request.method == "POST":
        # Проверяем ответы
        current_coins = 0
        for question, details in questions.items():
            answer = request.form.get(question)
            if answer:
                session["answers"][question] = answer
                
                # Начисляем монеты за правильные ответы
                if answer == details["correct_answer"]:
                    current_coins += 1
        
        # Обновляем количество монет
        session["coins"] = current_coins
        session["quiz_completed"] = True
        session.modified = True
        
        return render_template('quiz/index.html', 
                               questions=questions, 
                               coins=session["coins"], 
                               saved_answers=session["answers"],
                               quiz_completed=True)

    # GET-запрос
    saved_answers = session.get("answers", {})
    coins = session.get("coins", 0)
    quiz_completed = session.get("quiz_completed", False)

    return render_template('quiz/index.html', 
                           questions=questions, 
                           coins=coins, 
                           saved_answers=saved_answers,
                           quiz_completed=quiz_completed)

if __name__ == "__main__":
    app.run(debug=True)
