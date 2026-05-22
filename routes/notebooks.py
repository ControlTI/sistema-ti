from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from werkzeug.utils import secure_filename

from database.models import db
from database.models import Notebook

import pdfkit
import os

notebooks_bp = Blueprint(
    'notebooks',
    __name__
)

UPLOAD_FOLDER = 'uploads'

# =========================================================
# LISTAR NOTEBOOKS
# =========================================================

@notebooks_bp.route('/notebooks')
def notebooks():

    if 'usuario' not in session:

        return redirect('/')

    notebooks = Notebook.query.all()

    return render_template(
        'notebooks.html',
        notebooks=notebooks
    )

# =========================================================
# CADASTRAR NOTEBOOK
# =========================================================

@notebooks_bp.route(
    '/cadastrar_notebook',
    methods=['POST']
)
def cadastrar_notebook():

    termo = request.files['termo']

    nome_arquivo = ''

    # =====================================================
    # UPLOAD MANUAL
    # =====================================================

    if termo.filename != '':

        nome_arquivo = secure_filename(
            termo.filename
        )

        termo.save(
            os.path.join(
                UPLOAD_FOLDER,
                nome_arquivo
            )
        )

    # =====================================================
    # GERAR TERMO AUTOMÁTICO
    # =====================================================

    elif request.form.get('gerar_termo') == 'sim':

        html = render_template(

            'termo.html',

            colaborador=request.form['colaborador'],

            cpf=request.form['cpf'],

            area=request.form['area'],

            matricula=request.form['matricula'],

            notebook=request.form['notebook'],

            marca=request.form['marca'],

            modelo=request.form['modelo'],

            processador=request.form['processador'],

            serial=request.form['serial'],

            valor=request.form['valor'],

            tecnico=session['nome'],

            data=request.form['data'].split('-')[2] + '/' + request.form['data'].split('-')[1] + '/' + request.form['data'].split('-')[0]

        )

        config = pdfkit.configuration(

            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        )

        options = {

            'enable-local-file-access': ''

        }

        nome_arquivo = f'TERMO_{request.form["colaborador"]}.pdf'

        pdf_path = os.path.join(

            UPLOAD_FOLDER,
            nome_arquivo

        )

        pdfkit.from_string(

            html,
            pdf_path,
            configuration=config,
            options=options

        )

    # =====================================================
    # SALVAR BANCO
    # =====================================================

    novo = Notebook(

        colaborador=request.form['colaborador'],

        notebook=request.form['notebook'],

        marca=request.form['marca'],

        modelo=request.form['modelo'],

        processador=request.form['processador'],

        serial=request.form['serial'],

        status=request.form['status'],

        usuario=session['nome'],

        data=request.form['data'],

        observacoes=request.form['observacoes'],

        termo=nome_arquivo

    )

    db.session.add(novo)

    db.session.commit()

    return redirect('/notebooks')

# =========================================================
# EXCLUIR NOTEBOOK
# =========================================================

@notebooks_bp.route('/excluir_notebook/<int:id>')
def excluir_notebook(id):

    notebook = Notebook.query.get(id)

    if notebook:

        db.session.delete(notebook)

        db.session.commit()

    return redirect('/notebooks')

# =========================================================
# EDITAR NOTEBOOK
# =========================================================

@notebooks_bp.route(
    '/editar_notebook/<int:id>',
    methods=['GET', 'POST']
)
def editar_notebook(id):

    notebook = Notebook.query.get(id)

    if request.method == 'POST':

        notebook.colaborador = request.form['colaborador']

        notebook.notebook = request.form['notebook']

        notebook.marca = request.form['marca']

        notebook.modelo = request.form['modelo']

        notebook.processador = request.form['processador']

        notebook.serial = request.form['serial']

        notebook.status = request.form['status']

        notebook.data = request.form['data']

        notebook.observacoes = request.form['observacoes']

        db.session.commit()

        return redirect('/notebooks')

    return render_template(

        'editar_notebook.html',

        notebook=notebook

    )