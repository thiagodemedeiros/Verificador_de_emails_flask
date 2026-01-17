import json, time
from flask import Flask, request, Response
from flask_cors import CORS
from service.publisher_verificador_de_email import publisher_verificador_de_email

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "https://thiagodemedeiros.github.io"}},
    supports_credentials=True
)

@app.route('/')
def home():
    return "hello world"

@app.route('/verificar_email', methods=['POST'])
def verificar_email():
    data = request.get_json()

    if not data or "email" not in data:
        retorno = {"erro": "Campo 'email' é obrigatório"}
        return Response(
                    json.dumps(retorno, ensure_ascii=False),
                    content_type='application/json; charset=utf-8',
                    status=400
                )

    email = data["email"]

    if not isinstance(email, str) or not email.strip():
        retorno = {"erro": "Email inválido"}
        return Response(
                    json.dumps(retorno, ensure_ascii=False),
                    content_type='application/json; charset=utf-8',
                    status=400
                )

    print(email)
    email = request.args.get('email')

    if not email:
        data = {"erro": "Parâmetro 'email' é obrigatório"}
        return Response(
                    json.dumps(data, ensure_ascii=False),
                    content_type='application/json; charset=utf-8',
                    status=400
                )
    
    print(email)

    resposta = publisher_verificador_de_email(email)
    
    print(resposta)

    return Response(
                json.dumps(resposta, ensure_ascii=False),
                content_type='application/json; charset=utf-8',
                status=200
            )

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)