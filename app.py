from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL da API systeme.io
API_URL = "https://api.systeme.io/api/contacts"

# Chave de autenticação da API
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": "uliwgfxc19o8p00i1nsm67wa8hze0q3nqklek6vivdjwbgyd0lt1wz2uc1h8l7z0"
}

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Recebe o JSON do webhook, extrai o email e envia para a API systeme.io.
    """
    try:
        # Obtendo os dados do webhook
        data = request.json
        
        # Extraindo o email do JSON recebido
        email = data.get("data", {}).get("user", {}).get("email", None)

        # Se não houver email, retorna erro
        if not email:
            return jsonify({"error": "Email não encontrado"}), 400

        # Criando payload para API systeme.io
        payload = {
            "locale": "pt",
            "email": email
        }

        # Enviando requisição POST para a API
        response = requests.post(API_URL, json=payload, headers=HEADERS)

        # Retorna a resposta da API
        return jsonify({
            "status": response.status_code,
            "response": response.json()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)