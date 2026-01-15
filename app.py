import json
from flask import Flask, request, Response
from service.publisher_verificador_de_email import publisher_verificador_de_email

app = Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/verificar_email', methods=['GET'])
def verificar_email():
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