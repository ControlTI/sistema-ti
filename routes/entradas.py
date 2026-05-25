from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from routes.models import db, Entrada

entradas_bp = Blueprint(
    'entradas',
    __name__
)

# =====================================================
# ENTRADAS
# =====================================================

@entradas_bp.route('/entradas')
def entradas():

    if 'usuario' not in session:

        return redirect('/')

    entradas = Entrada.query.all()

    return render_template(

        'entradas.html',

        entradas=entradas

    )
# =====================================================
# CADASTRAR ENTRADA
# =====================================================

@entradas_bp.route(
    '/cadastrar_entrada',
    methods=['POST']
)
def cadastrar_entrada():

    nova_entrada = Entrada(

    produto=request.form['produto'],

    marca=request.form['marca'],

    categoria=request.form['categoria'],

    quantidade=request.form['quantidade'],

    fornecedor=request.form['fornecedor'],

    nota_fiscal=request.form['nota_fiscal'],

    status=request.form['status'],

    usuario=session['nome'],

    data=request.form['data']

    )

    db.session.add(nova_entrada)

    db.session.commit()

    return redirect('/entradas')