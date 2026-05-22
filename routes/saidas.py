from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from database.models import db
from database.models import Saida

saidas_bp = Blueprint(
    'saidas',
    __name__
)

# =====================================================
# SAIDAS
# =====================================================

@saidas_bp.route('/saidas')
def saidas():

    saidas = Saida.query.all()

    return render_template(

        'saidas.html',

        saidas=saidas

    )

# =====================================================
# CADASTRAR SAIDA
# =====================================================

@saidas_bp.route(
    '/cadastrar_saida',
    methods=['POST']
)
def cadastrar_saida():

    nova_saida = Saida(

        produto=request.form['produto'],

        quantidade=request.form['quantidade'],

        destino=request.form['destino'],

        observacao=request.form['observacao'],

        usuario=session['nome'],

        data=request.form['data']

    )

    db.session.add(nova_saida)

    db.session.commit()

    return redirect('/saidas')