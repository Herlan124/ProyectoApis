from flask import Flask
from modelo.modeloCliente import ClienteModel
from decouple import config
from flask_cors import CORS
app = Flask(__name__)	

@app.route('/')
def hello_world():
        return 'hola INF530'

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    emp = ClienteModel.listar_cliente()
    return emp

@app.route('/clientes', methods=['POST'])
def crear_clientes():
    emp = ClienteModel.registrar_cliente()
    return emp

@app.route('/clientes', methods=['PUT'])
def modificar_clientes():
    emp = ClienteModel.modificar_cliente()
    return emp

if __name__ == '__main__':
   		app.run(debug=True,host='0.0.0.0') 