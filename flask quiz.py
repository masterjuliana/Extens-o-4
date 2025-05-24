from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Carregar o banco de questões
def load_questions(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar o arquivo JSON '{filename}'.")
        return []

# Carregar as questões
banco_de_questoes = load_questions("banco_de_questoes_hidraulica.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', banco_de_questoes=banco_de_questoes)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    question_index = int(request.form['question_index'])
    user_answer = request.form['user_answer']
    correct_answer = banco_de_questoes[question_index]["resposta_correta"]
    
    feedback = banco_de_questoes[question_index]["feedback"]
    result = "Correto" if user_answer == correct_answer else "Errado"
    
    return jsonify({
        'result': result,
        'feedback': feedback
    })

if __name__ == "__main__":
    app.run(debug=True)
