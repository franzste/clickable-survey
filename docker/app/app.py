import random
import time
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def remove_permissions_policy_header(response):
    response.headers.remove('Permissions-Policy')
    return response

@app.route('/')
def index():
    with open('/import/survey_text.txt', 'r') as file:
        survey_text = file.read()
        # Ersetze Zeilenumbrüche durch <br> Tags
        survey_text = survey_text.replace('\n', '<br>')


    # TODO: server_ip dynamisch setzen
    return render_template('index.html', server_ip='http://192.168.178.171:5000', survey_heading='Umfrage 1', survey_description='Bitte beantworte die folgenden Fragen:',
        survey_text=survey_text
            )

@app.route('/api/words', methods=['POST'])
def save_words():
    data = request.get_json()

   # Überprüfe, ob die erforderlichen Schlüssel im JSON vorhanden sind
    if 'abschluss' not in data or 'words' not in data:
        return jsonify({'error': 'Missing data'}), 400

    abschluss = data['abschluss']

    words = data.get('words')
    if words:
        # Hier kannst du die Logik hinzufügen, um die Wörter zu speichern oder weiterzuverarbeiten
        print("Empfangene Wörter:", words)

        # TODO: besseren weg finden um die Datei zu benennen und eindeutig zu machen
        # TODO: refactor in eine Funktion um den try catch block auszulagern
        # generiere eine zufällige Zahl
        random_number = random.randint(1, 100000000000) + time.time().as_integer_ratio()[0]

        # prüfe ob die Datei schon existiert
        try:
            with open(f'/export/survey-{random_number}.csv', 'x') as file:
                pass
        except FileExistsError:
            random_number = random.randint(1, 100000000000) + time.time().as_integer_ratio()[0]
            pass

        # Speicher jedes wort und dessen position in csv
        with open(f'/export/survey-{random_number}.csv', 'a') as file:
            file.write(f'abschluss\n{abschluss}\n')
            file.write('word,position\n')
            for word_obj in words:
                file.write(f'{word_obj["word"]},{word_obj["position"]}\n')


        return jsonify({'message': 'Wörter erfolgreich empfangen.'}), 200
    else:
        return jsonify({'error': 'Keine Wörter empfangen.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')