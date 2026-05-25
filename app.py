from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_from_directory
)

import sqlite3
import os

# =====================================================
# SQLALCHEMY
# =====================================================

from routes.models import (
    db,
    Produto,
    Usuario,
    Movimentacao,
    Notebook
)

# =====================================================
# APP
# =====================================================

app = Flask(__name__)

app.secret_key = 'allied_sistema'

# =====================================================
# SQLALCHEMY CONFIG
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' +
    os.path.join(BASE_DIR, 'sistema.db')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================================
# UPLOADS
# =====================================================

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =====================================================
# INIT DB
# =====================================================

db.init_app(app)

# =====================================================
# CRIAR TABELAS
# =====================================================

with app.app_context():

    db.create_all()

# =====================================================
# REGISTRAR ROTAS
# =====================================================

from routes.estoque import estoque_bp
from routes.entradas import entradas_bp
from routes.saidas import saidas_bp
from routes.notebooks import notebooks_bp

app.register_blueprint(estoque_bp)
app.register_blueprint(entradas_bp)
app.register_blueprint(saidas_bp)
app.register_blueprint(notebooks_bp)

# =====================================================
# BANCO SQLITE
# =====================================================

conn = sqlite3.connect('sistema.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    nome TEXT,
    senha TEXT,
    nivel TEXT,
    filial TEXT
)
''')

usuarios = [

    ('bsantos', 'Brenda', 'Breset11!', 'Admin', 'Robocop'),

    ('mmarques', 'Matheus', '1234', 'Tecnico', 'Robocop'),
    ('gasantos', 'Gabriel', '1235', 'Tecnico', 'Robocop'),
    ('wsalves', 'Welbert', '1236', 'Tecnico', 'Robocop'),

    ('t_noliveira', 'Nicollas', '1234', 'Tecnico', 'Jundiai'),

    ('pacruz', 'Pablo', '1234', 'Tecnico', 'Serra'),
    ('lgnascimento', 'Lucas', '1234', 'Tecnico', 'Serra')

]

for usuario in usuarios:

    c.execute(
        "SELECT * FROM usuarios WHERE usuario=?",
        (usuario[0],)
    )

    existe = c.fetchone()

    if not existe:

        c.execute(
            """
            INSERT INTO usuarios
            (usuario, nome, senha, nivel, filial)
            VALUES (?, ?, ?, ?, ?)
            """,
            usuario
        )

conn.commit()
conn.close()

# =====================================================
# LOGIN
# =====================================================

@app.route('/', methods=['GET', 'POST'])
def login():

    erro = False

    if request.method == 'POST':

        usuario = request.form['usuario']
        senha = request.form['senha']
        filial = request.form['filial']

        conn = sqlite3.connect('sistema.db')
        c = conn.cursor()

        c.execute(
            """
            SELECT * FROM usuarios
            WHERE usuario=? AND senha=? AND filial=?
            """,
            (usuario, senha, filial)
        )

        user = c.fetchone()

        conn.close()

        if user:

            session['usuario'] = user[1]
            session['nome'] = user[2]
            session['nivel'] = user[4]
            session['filial'] = filial

            return redirect('/home')

        else:

            erro = True

    return render_template(
        'login.html',
        erro=erro
    )

# =====================================================
# CRIAR USUÁRIO
# =====================================================

@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():

    nome = request.form['nome']
    usuario = request.form['usuario']
    senha = request.form['senha']
    filial = request.form['filial']

    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO usuarios
        (usuario, nome, senha, nivel, filial)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            usuario,
            nome,
            senha,
            'Tecnico',
            filial
        )
    )

    conn.commit()
    conn.close()

    return redirect('/')

# =====================================================
# TROCAR SENHA
# =====================================================

@app.route('/trocar_senha', methods=['POST'])
def trocar_senha():

    usuario = request.form['usuario']
    nova_senha = request.form['nova_senha']

    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()

    c.execute(
        """
        UPDATE usuarios
        SET senha=?
        WHERE usuario=?
        """,
        (nova_senha, usuario)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# =====================================================
# HOME
# =====================================================

@app.route('/home')
def home():

    if 'usuario' not in session:

        return redirect('/')

    return render_template('home.html')

# =====================================================
# UPLOADS
# =====================================================

@app.route('/uploads/<filename>')
def upload(filename):

    return send_from_directory(
        'uploads',
        filename
    )

# =====================================================
# START
# =====================================================

if __name__ == '__main__':

    app.run(
        debug=True
    )
@app.route('/uploads/<path:filename>')
def arquivos_upload(filename):

    return send_from_directory(

        'uploads',

        filename

    )