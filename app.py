from flask import Flask, request
import sett 
app = Flask(__name__)


@app.route('/welcome', methods=['GET'])
def index():
    return '<p>En el comienzo era el verbo y el verbo se hizo carne!</p>'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto'



    except exception as e:


if __name__ == '__main__':
    app.run(port=3000)
