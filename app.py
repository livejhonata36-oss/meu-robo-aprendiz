from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

ARQUIVO_MEMORIA = "memoria.json"

# cria memória se não existir
if not os.path.exists(ARQUIVO_MEMORIA):
    with open(ARQUIVO_MEMORIA, "w") as f:
        json.dump({}, f)

def carregar_memoria():
    with open(ARQUIVO_MEMORIA, "r") as f:
        return json.load(f)

def salvar_memoria(memoria):
    with open(ARQUIVO_MEMORIA, "w") as f:
        json.dump(memoria, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mensagem", methods=["POST"])
def mensagem():
    dados = request.json
    texto = dados["texto"].lower()

    memoria = carregar_memoria()

    if texto in memoria:
        return jsonify({"resposta": memoria[texto]})
    else:
        return jsonify({"resposta": "Eu não sei responder isso 😅 Como eu deveria responder?"})

@app.route("/aprender", methods=["POST"])
def aprender():
    dados = request.json
    pergunta = dados["pergunta"].lower()
    resposta = dados["resposta"]

    memoria = carregar_memoria()
    memoria[pergunta] = resposta
    salvar_memoria(memoria)

    return jsonify({"status": "aprendido"})

if __name__ == "__main__":
    app.run(debug=True)