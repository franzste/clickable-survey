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
    return render_template('index.html', server_ip='http://192.168.178.171:5000', survey_heading='Umfrage 1', survey_description='Bitte beantworte die folgenden Fragen:',
        survey_text=
        '''
        Das ist mein Beispieltext. Hier kannst du die Umfragebeschreibung hinzufügen. Lorem Ipsum dolor sit amet.
        '''
            )

@app.route('/api/words', methods=['POST'])
def save_words():
    data = request.get_json()
    words = data.get('words')
    if words:
        # Hier kannst du die Logik hinzufügen, um die Wörter zu speichern oder weiterzuverarbeiten
        print("Empfangene Wörter:", words)


        return jsonify({'message': 'Wörter erfolgreich empfangen.'}), 200
    else:
        return jsonify({'error': 'Keine Wörter empfangen.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')