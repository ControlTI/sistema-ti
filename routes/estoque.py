from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from database.models import db
from database.models import Produto

estoque_bp = Blueprint(
    'estoque',
    __name__
)

# =====================================================
# ESTOQUE
# =====================================================

@estoque_bp.route('/estoque')
def estoque():

    if 'usuario' not in session:

        return redirect('/')

    produtos = Produto.query.all()

    return render_template(

        'estoque.html',

        produtos=produtos

    )

# =====================================================
# CADASTRAR PRODUTO
# =====================================================

@estoque_bp.route(
    '/cadastrar_produto',
    methods=['POST']
)
def cadastrar_produto():

    novo_produto = Produto(

        nome=request.form['nome'],

        marca=request.form['marca'],

        categoria=request.form['categoria'],

        quantidade=request.form['quantidade'],

        fornecedor=request.form['fornecedor'],

        nota_fiscal=request.form['nota_fiscal'],

        serial=request.form['serial'],

        patrimonio=request.form['patrimonio'],

        observacoes=request.form['observacoes'],

        status=request.form['status'],

        usuario=session['nome'],

        data=request.form['data'],

        estoque_minimo=1

    )

    db.session.add(novo_produto)

    db.session.commit()

    return redirect('/estoque')

# =====================================================
# EXCLUIR PRODUTO
# =====================================================

@estoque_bp.route('/excluir_produto/<int:id>')
def excluir_produto(id):

    if 'usuario' not in session:

        return redirect('/')

    produto = Produto.query.get_or_404(id)

    db.session.delete(produto)

    db.session.commit()

    return redirect('/estoque')

# =====================================================
# EDITAR PRODUTO
# =====================================================

@estoque_bp.route(
    '/editar_produto/<int:id>',
    methods=['POST']
)
def editar_produto(id):

    produto = Produto.query.get_or_404(id)

    produto.nome = request.form['nome']

    produto.marca = request.form['marca']

    produto.categoria = request.form['categoria']

    produto.quantidade = request.form['quantidade']

    produto.fornecedor = request.form['fornecedor']

    produto.nota_fiscal = request.form['nota_fiscal']

    produto.serial = request.form['serial']

    produto.patrimonio = request.form['patrimonio']

    produto.observacoes = request.form['observacoes']

    produto.status = request.form['status']

    produto.usuario = session['nome']

    produto.data = request.form['data']

    db.session.commit()

    return redirect('/estoque')