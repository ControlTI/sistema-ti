from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# =====================================================
# PRODUTOS
# =====================================================

class Produto(db.Model):

    __tablename__ = 'produtos'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100)
    )

    marca = db.Column(
        db.String(100)
    )

    categoria = db.Column(
        db.String(200)
    )

    quantidade = db.Column(
        db.Integer
    )

    fornecedor = db.Column(
        db.String(100)
    )

    nota_fiscal = db.Column(
        db.String(100)
    )

    processador = db.Column(
        db.String(100)
    )

    serial = db.Column(
        db.String(100)
    )

    observacoes = db.Column(
        db.Text
    )

    estoque_minimo = db.Column(
        db.Integer
    )

    status = db.Column(
        db.String(50)
    )

    usuario = db.Column(
        db.String(100)
    )

    data = db.Column(
        db.String(100)
    )

# =====================================================
# USUÁRIOS
# =====================================================

class Usuario(db.Model):

    __tablename__ = 'usuarios'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario = db.Column(
        db.String(50)
    )

    nome = db.Column(
        db.String(100)
    )

    senha = db.Column(
        db.String(100)
    )

    nivel = db.Column(
        db.String(50)
    )

    filial = db.Column(
        db.String(50)
    )

# =====================================================
# MOVIMENTAÇÕES
# =====================================================

class Movimentacao(db.Model):

    __tablename__ = 'movimentacoes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    tipo = db.Column(
        db.String(20)
    )

    produto = db.Column(
        db.String(100)
    )

    quantidade = db.Column(
        db.Integer
    )

    usuario = db.Column(
        db.String(100)
    )

    data = db.Column(
        db.String(20)
    )

# =====================================================
# ENTRADAS
# =====================================================

class Entrada(db.Model):

    __tablename__ = 'entradas'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    produto = db.Column(
        db.String(100)
    )

    marca = db.Column(
        db.String(100)
    )

    categoria = db.Column(
        db.String(200)
    )

    quantidade = db.Column(
        db.Integer
    )

    fornecedor = db.Column(
        db.String(100)
    )

    nota_fiscal = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50)
    )

    usuario = db.Column(
        db.String(100)
    )

    data = db.Column(
        db.String(100)
    )

# =====================================================
# SAIDAS
# =====================================================

class Saida(db.Model):

    __tablename__ = 'saidas'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    produto = db.Column(
        db.String(100)
    )

    quantidade = db.Column(
        db.Integer
    )

    destino = db.Column(
        db.String(100)
    )

    observacao = db.Column(
        db.Text
    )

    usuario = db.Column(
        db.String(100)
    )

    data = db.Column(
        db.String(100)
    )

# =====================================================
# NOTEBOOKS
# =====================================================

class Notebook(db.Model):

    __tablename__ = 'notebooks'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    colaborador = db.Column(
        db.String(100)
    )

    token = db.Column(
    db.String(120),
    unique=True

    )
    notebook = db.Column(
        db.String(100)
    )

    marca = db.Column(
        db.String(100)
    )

    modelo = db.Column(
        db.String(100)
    )

    processador = db.Column(
        db.String(100)
    )

    serial = db.Column(
        db.String(100)
    )

    cpf = db.Column(
        db.String(50)
    )

    area = db.Column(
        db.String(100)
    )

    matricula = db.Column(
        db.String(100)
    )

    valor = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50)
    )

    termo = db.Column(
       db.String(200)

    )

    assinatura = db.Column(
       db.String(200)

    )

    usuario = db.Column(
        db.String(100)
    )

    data = db.Column(
        db.String(100)
    )

    observacoes = db.Column(
        db.Text
    )
    
