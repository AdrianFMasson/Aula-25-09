from models import cliente_model


def _validar_dados(dados):
    """Valida se os campos obrigatórios foram preenchidos"""
    nome = (dados.get('nome') or '').strip()
    email = (dados.get('email') or '').strip()
    telefone = (dados.get('telefone') or '').strip()
    cidade = (dados.get('cidade') or '').strip()

    if not nome or not email or not telefone or not cidade:
        return None, {'erro': 'Todos os campos (nome, email, telefone, cidade) são obrigatórios.'}

    return {'nome': nome, 'email': email, 'telefone': telefone, 'cidade': cidade}, None


def get_clientes():
    """Regra de negócio para listagem de clientes"""
    return cliente_model.listar_clientes()


def post_cliente(dados):
    """Regra de negócio para cadastro de um novo cliente"""
    if not dados:
        return {'erro': 'Nenhum dado enviado.'}, 400

    dados_validos, erro = _validar_dados(dados)
    if erro:
        return erro, 400

    novo_id = cliente_model.inserir_cliente(
        dados_validos['nome'],
        dados_validos['email'],
        dados_validos['telefone'],
        dados_validos['cidade']
    )

    return {'id': novo_id, **dados_validos}, 201


def put_cliente(id_cliente, dados):
    """Regra de negócio para atualização de um cliente existente"""
    if not dados:
        return {'erro': 'Nenhum dado enviado.'}, 400

    dados_validos, erro = _validar_dados(dados)
    if erro:
        return erro, 400

    linhas = cliente_model.atualizar_cliente(
        id_cliente,
        dados_validos['nome'],
        dados_validos['email'],
        dados_validos['telefone'],
        dados_validos['cidade']
    )

    if linhas == 0:
        return {'erro': 'Cliente não encontrado.'}, 404

    return {'id': id_cliente, **dados_validos}, 200


def delete_cliente(id_cliente):
    """Regra de negócio para remoção de um cliente"""
    linhas = cliente_model.deletar_cliente(id_cliente)
    if linhas == 0:
        return {'erro': 'Cliente não encontrado.'}, 404
    return {'mensagem': 'Cliente removido com sucesso.'}, 200
