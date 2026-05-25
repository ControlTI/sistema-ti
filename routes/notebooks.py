from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

import smtplib
import os
import uuid

os.makedirs(

    'uploads',

    exist_ok=True

)

import uuid

from email.mime.text import MIMEText

from werkzeug.utils import secure_filename

from routes.models import db, Notebook

notebooks_bp = Blueprint(
    'notebooks',
    __name__
)

# =====================================================
# DETECTA RENDER
# =====================================================

RENDER = os.environ.get("RENDER")

# =====================================================
# LISTAR
# =====================================================

@notebooks_bp.route('/notebooks')
def notebooks():

    if 'usuario' not in session:

        return redirect('/')

    notebooks = Notebook.query.all()

    return render_template(

        'notebooks.html',

        notebooks=notebooks

    )

# =====================================================
# CARREGANDO
# =====================================================

@notebooks_bp.route('/carregando/<token>')
def carregando(token):

    return render_template(

        'carregando.html',

        token=token

    )

# =====================================================
# CADASTRAR
# =====================================================

@notebooks_bp.route(
    '/cadastrar_notebook',
    methods=['POST']
)
def cadastrar_notebook():

    nome_arquivo = ''

    tipo_termo = request.form.get(

        'tipo_termo'

    )

    # =====================================================
    # GERAR TERMO
    # =====================================================

    if tipo_termo == 'gerar':

        html = render_template(

            'termo.html',

            colaborador=request.form['colaborador'],
            cpf=request.form.get('cpf'),
            area=request.form.get('area'),
            matricula=request.form.get('matricula'),
            notebook=request.form['notebook'],
            marca=request.form['marca'],
            modelo=request.form['modelo'],
            serial=request.form['serial'],
            valor=request.form.get('valor'),
            data=request.form['data']

        )

        nome_arquivo = (

            f"TERMO_{uuid.uuid4().hex}.pdf"

        )

        pdf_path = os.path.join(

            'uploads',

            nome_arquivo

        )

    if RENDER:

        from weasyprint import HTML

        HTML(

            string=html

        ).write_pdf(

            pdf_path

        )

    # =====================================================
    # ANEXAR PDF
    # =====================================================

    elif 'termo' in request.files:

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
    # SALVAR
    # =====================================================

    novo = Notebook(

        token=uuid.uuid4().hex,

        colaborador=request.form['colaborador'],

        notebook=request.form['notebook'],

        marca=request.form['marca'],

        modelo=request.form['modelo'],

        processador=request.form['processador'],

        serial=request.form['serial'],

        cpf=request.form.get('cpf'),

        area=request.form.get('area'),

        matricula=request.form.get('matricula'),

        valor=request.form.get('valor'),

        status=request.form['status'],

        usuario=session['nome'],

        data=request.form['data'],

        observacoes=request.form['observacoes'],

        termo=nome_arquivo

    )

    db.session.add(novo)

    db.session.commit()

    # =====================================================
    # EMAIL AUTOMÁTICO
    # =====================================================

    try:

        msg = MIMEText(f"""

<html>

<body style="font-family:Arial;background:#f4f7fb;padding:30px;">

<div style="background:white;border-radius:20px;padding:40px;max-width:600px;margin:auto;">

<h2 style="color:#071b45;">

Assinatura de Termo

</h2>

<p>

Olá {novo.colaborador},

</p>

<p>

Seu termo está disponível para assinatura digital.

</p>

<a

href="https://sistema-ti-546b.onrender.com/carregando/{novo.token}"

style="display:inline-block;margin-top:20px;background:#2563eb;color:white;text-decoration:none;padding:14px 24px;border-radius:12px;font-weight:bold;"

>

ASSINAR TERMO

</a>

<p style="margin-top:30px;color:#6b7280;font-size:13px;">

Por segurança, será necessário validar seu CPF.

</p>

</div>

</body>

</html>

""", 'html')

        msg['Subject'] = 'Assinatura de Termo'

        msg['From'] = 'sistematiempresa@gmail.com'

        msg['To'] = request.form['email_destino']

        server = smtplib.SMTP(

            'smtp.gmail.com',
            587

        )

        server.starttls()

        server.login(

            'sistematiempresa@gmail.com',

            'iuiy wzgb mbcw lrju'

        )

        server.send_message(msg)

        server.quit()

    except Exception as erro:

        print(

            'ERRO EMAIL:',
            erro

        )

    return redirect('/notebooks')

# =====================================================
# EDITAR
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

# =====================================================
# EXCLUIR
# =====================================================

@notebooks_bp.route('/excluir_notebook/<int:id>')
def excluir_notebook(id):

    notebook = Notebook.query.get_or_404(id)

    db.session.delete(notebook)

    db.session.commit()

    return redirect('/notebooks')

# =====================================================
# ASSINAR
# =====================================================

@notebooks_bp.route(
    '/assinar/<token>',
    methods=['GET', 'POST']
)
def assinar(token):

    notebook = Notebook.query.filter_by(
        token=token
    ).first_or_404()

    liberado = False

    if request.method == 'POST':

        cpf_digitado = request.form['cpf']

        cpf_limpo = cpf_digitado.replace(
            '.', ''
        ).replace(
            '-', ''
        )

        cpf_banco = notebook.cpf.replace(
            '.', ''
        ).replace(
            '-', ''
        )

        if cpf_limpo == cpf_banco:

            liberado = True

    return render_template(

        'assinar.html',

        notebook=notebook,

        liberado=liberado

    )

# =====================================================
# SALVAR ASSINATURA
# =====================================================

@notebooks_bp.route(
    '/salvar_assinatura/<int:id>',
    methods=['POST']
)
def salvar_assinatura(id):

    notebook = Notebook.query.get_or_404(id)

    assinatura = request.form['assinatura']

    notebook.assinatura = assinatura

    db.session.commit()

    return {

        'status': 'ok'

    }