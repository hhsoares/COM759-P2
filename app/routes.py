from flask import json, request, jsonify
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId

# List all notas fiscais
@app.route('/')
@app.route('/index')
def index():
    notas = db.notafiscal.find({}).sort("_id", 1)
    return flask.jsonify(json.loads(json_util.dumps(notas)))

# Render create form
@app.route("/create")
def create():
    return flask.render_template('create.html')

# Create new nota fiscal
@app.route('/createAction', methods=['POST'])
def createAction():
    json_data = request.form.to_dict()
    if json_data:
        if db.notafiscal.insert_one(json_data).inserted_id:
            return jsonify(mensagem='Nota fiscal inserida com sucesso!')
        else:
            return jsonify(mensagem='Erro ao inserir nota fiscal.')
    else:
        return jsonify(mensagem='Nenhum dado recebido.')

# Render update form
@app.route("/update/<string:numero>")
def update(numero):
    nota = db.notafiscal.find_one({"numero": numero})
    if nota:
        return flask.render_template('update.html', nota=nota)
    else:
        return jsonify(mensagem='Nota fiscal não encontrada.')

# Update existing nota fiscal
@app.route('/updateAction', methods=['POST'])
def updateAction():
    json_data = request.form.to_dict()
    if json_data and "_id" in json_data:
        updated_data = {
            'numero': json_data.get('numero'),
            'comprador': json_data.get('comprador'),
            'cnpj': json_data.get('cnpj'),
            'endereco': json_data.get('endereco'),
            'telefone': json_data.get('telefone'),
            'data': json_data.get('data'),
            'valor': json_data.get('valor'),
            'itens': json_data.get('itens')
        }
        result = db.notafiscal.update_one(
            {'_id': ObjectId(json_data['_id'])},
            {"$set": updated_data}
        )
        if result.modified_count > 0:
            return jsonify(mensagem='Nota fiscal alterada com sucesso!')
        else:
            return jsonify(mensagem='Nenhuma alteração feita.')
    else:
        return jsonify(mensagem='Dados inválidos para atualização.')

# Delete nota fiscal
@app.route("/delete/<string:numero>")
def delete(numero):
    result = db.notafiscal.delete_one({"numero": numero})
    if result.deleted_count > 0:
        return jsonify(mensagem='Nota fiscal removida com sucesso!')
    else:
        return jsonify(mensagem='Nota fiscal não encontrada para remoção.')
