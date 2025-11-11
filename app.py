# Imports
from flask import Flask, render_template, session, redirect, request, url_for, jsonify
import json
import os
from flask_cors import CORS
# Переменные
app = Flask(__name__)
SCHEDULE_FILE = 'schedule.json'
app.secret_key = 'RlaGw60C3Ql2i1jlVH0dv583h8m64y8tolansvrwyKQdD9HisrVXvCpB2VMqUE46xMMjckKAPdcPOLANJsmaHAUFmyV'
USER_NAME = 'shabdan'
PASSWORD = '2011'

# Routs


@app.route('/')
def index():
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        schedule_data = json.load(f)
    logged_in = session.get('logged_in', False)
    return render_template('index.html', schedule=schedule_data, logged_in=logged_in, name="Главная")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER_NAME and password == PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверный логин или пароль', name="Войти")

    return render_template('login.html', name= "Войти")


@app.route('/edit', methods=['GET', 'POST'])
def edit_schedule():
    if "logged_in" not in session or not session["logged_in"]:
        return redirect(url_for('login'))

    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        schedule_data = json.load(f)

    if request.method == 'POST':
        # Первая смена
        for i in range(len(schedule_data['shift_1'])):
            #schedule_data['shift_1'][i]['lesson'] = int(request.form[f'shift_1_lesson_{i}'])
            schedule_data['shift_1'][i]['start'] = request.form[f'shift_1_start_{i}']
            schedule_data['shift_1'][i]['end'] = request.form[f'shift_1_end_{i}']

        # Вторая смена
        for i in range(len(schedule_data['shift_2'])):
            #schedule_data['shift_2'][i]['lesson'] = int(request.form[f'shift_2_lesson_{i}'])
            schedule_data['shift_2'][i]['start'] = request.form[f'shift_2_start_{i}']
            schedule_data['shift_2'][i]['end'] = request.form[f'shift_2_end_{i}']

        # Сохранить изменения
        with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('edit.html', schedule=schedule_data, name="Редактирование")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/save_schedule', methods=['POST'])
def save_schedule():
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        schedule_data = json.load(f)

    # Обновляем первую смену
    for i in range(len(schedule_data['shift_1'])):
        schedule_data['shift_1'][i]['lesson'] = request.form.get(f'shift_1_lesson_{i}')
        schedule_data['shift_1'][i]['start'] = request.form.get(f'shift_1_start_{i}')
        schedule_data['shift_1'][i]['end'] = request.form.get(f'shift_1_end_{i}')

    # Обновляем вторую смену
    for i in range(len(schedule_data['shift_2'])):
        schedule_data['shift_2'][i]['lesson'] = request.form.get(f'shift_2_lesson_{i}')
        schedule_data['shift_2'][i]['start'] = request.form.get(f'shift_2_start_{i}')
        schedule_data['shift_2'][i]['end'] = request.form.get(f'shift_2_end_{i}')

    # Сохраняем файл
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule_data, f, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))

@app.route('/dict')
def dict():
    return render_template('dictophone.html')

@app.route('/api/schedule', methods=['GET'])
def api_schedule():
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        schedule_data = json.load(f)
    return jsonify(schedule_data)




CORS(app)  # разрешаем CORS для JS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/upload", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, "latest.webm")
        file.save(file_path)
        print(f"🎧 Аудио сохранено: {file_path}")
        return {"status": "success"}, 200
    return {"status": "no file"}, 400


# Start
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
