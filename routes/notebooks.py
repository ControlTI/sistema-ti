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

import os
import pdfkit
import win32com.client
import pythoncom

notebooks_bp = Blueprint(
    'notebooks',
    __name__
)

# =====================================================
# NOTEBOOKS
# =====================================================

@notebooks_bp.route('/notebooks')
def notebooks():

    notebooks = Notebook.query.all()

    return render_template(

        'notebooks.html',

        notebooks=notebooks

    )

# =====================================================
# CADASTRAR NOTEBOOK
# =====================================================

@notebooks_bp.route(
    '/cadastrar_notebook',
    methods=['POST']
)
def cadastrar_notebook():

    nome_arquivo = ''

    # =====================================================
    # UPLOAD MANUAL
    # =====================================================

    if 'termo' in request.files:

        arquivo = request.files['termo']

        if arquivo.filename != '':

            nome_arquivo = secure_filename(

                arquivo.filename

            )

            caminho = os.path.join(

                'uploads',

                nome_arquivo

            )

            arquivo.save(caminho)

    # =====================================================
    # GERAR TERMO
    # =====================================================

    if request.form.get('gerar_termo') == 'sim':

        nome_arquivo = (

            f'TERMO_{request.form["colaborador"]}.pdf'

        )

        html = render_template(

        'termo.html',

        colaborador=request.form['colaborador'],

        cpf=request.form['cpf'],

        area=request.form['area'],

        tecnico=session['nome'],

        matricula=request.form['matricula'],

        notebook=request.form['notebook'],

        marca=request.form['marca'],

        modelo=request.form['modelo'],

        processador=request.form['processador'],

        serial=request.form['serial'],

        valor=request.form['valor'],

        data=request.form['data'].split('-')[2] + '/' + request.form['data'].split('-')[1] + '/' + request.form['data'].split('-')[0]

        )

        config = pdfkit.configuration(

            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        )

        options = {

            'enable-local-file-access': None

        }

        pdfkit.from_string(

            html,

            f'uploads/{nome_arquivo}',

            configuration=config,

            options=options

        )

    # =====================================================
    # SALVAR NO BANCO
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

    # =====================================================
    # OUTLOOK EMAIL
    # =====================================================

    if nome_arquivo != '':

        pythoncom.CoInitialize()

        outlook = win32com.client.Dispatch(

            'outlook.application'

        )

        mail = outlook.CreateItem(0)

        mail.To = request.form['email_destino']

        mail.Subject = (

            'Termo de Entrega de Equipamento'

        )

        mail.HTMLBody = f"""

        <p>Olá,</p>

        <p>

        Segue em anexo o termo de entrega do equipamento disponibilizado.

        </p>

        <p>

        <b>Equipamento:</b>
        {request.form['notebook']}

        <br>

        <b>Serial:</b>
        {request.form['serial']}

        </p>

        <p>

        Por gentileza, valide as informações.
        Estando tudo correto, responda este e-mail
        com um “de acordo”.

        Em caso de divergências,
        entre em contato conosco para realização
        dos ajustes necessários.

        </p>

        <p>

        Atenciosamente,
        <br>
        TI - Allied

        </p>

        """

        pdf_path = os.path.abspath(

            f'uploads/{nome_arquivo}'

        )

        mail.Attachments.Add(pdf_path)

        mail.Display()

    return redirect('/notebooks')

# =====================================================
# EXCLUIR NOTEBOOK
# =====================================================

@notebooks_bp.route('/excluir_notebook/<int:id>')
def excluir_notebook(id):

    notebook = Notebook.query.get_or_404(id)

    db.session.delete(notebook)

    db.session.commit()

    return redirect('/notebooks')

# =====================================================
# EDITAR NOTEBOOK
# =====================================================

@notebooks_bp.route(
    '/editar_notebook/<int:id>',
    methods=['GET', 'POST']
)
def editar_notebook(id):

    notebook = Notebook.query.get_or_404(id)

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