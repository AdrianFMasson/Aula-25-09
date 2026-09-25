from flask import Blueprint, jsonify, request
from controllers import cliente_controller

cliente_bp = Blueprint('cliente_bp', __name__)


@cliente_bp.route('/api/clientes', methods=['GET'])
def listar():
    """GET - lista todos os clientes cadastrados"""
    try:
        clientes = cliente_controller.get_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar clientes: {str(e)}'}), 500


@cliente_bp.route('/api/clientes', methods=['POST'])
def cadastrar():
    """POST - cadastra um novo cliente"""
    try:
        dados = request.get_json(silent=True)
        resposta, status = cliente_controller.post_cliente(dados)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({'erro': f'Erro ao cadastrar cliente: {str(e)}'}), 500


@cliente_bp.route('/api/clientes/<int:id_cliente>', methods=['PUT'])
def atualizar(id_cliente):
    """PUT - atualiza os dados de um cliente pelo ID"""
    try:
        dados = request.get_json(silent=True)
        resposta, status = cliente_controller.put_cliente(id_cliente, dados)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar cliente: {str(e)}'}), 500


@cliente_bp.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])
def deletar(id_cliente):
    """DELETE - remove um cliente pelo ID"""
    try:
        resposta, status = cliente_controller.delete_cliente(id_cliente)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({'erro': f'Erro ao remover cliente: {str(e)}'}), 500
