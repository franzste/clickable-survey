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
    # TODO: server_ip dynamisch setzen
    return render_template('index.html', server_ip='http://192.168.178.171:5000', survey_heading='Umfrage 1', survey_description='Bitte beantworte die folgenden Fragen:',
        survey_text=
        '''
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
        '''
            )

@app.route('/api/words', methods=['POST'])
def save_words():
    data = request.get_json()
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
            with open(f'survey-{random_number}.csv', 'x') as file:
                file.write('word,position\n')
        except FileExistsError:
            random_number = random.randint(1, 100000000000) + time.time().as_integer_ratio()[0]
            pass

        # Speicher jedes wort und dessen position in csv
        with open(f'survey-{random_number}.csv', 'a') as file:
            for word_obj in words:
                file.write(f'{word_obj["word"]},{word_obj["position"]}\n')


        return jsonify({'message': 'Wörter erfolgreich empfangen.'}), 200
    else:
        return jsonify({'error': 'Keine Wörter empfangen.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')