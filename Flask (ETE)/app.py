from flask import Flask, render_template, request, redirect,url_for 
import base64

import sqlite3

#cria o objeto app
app = Flask(__name__ , static_folder='static')


# conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database\sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para o painel de administração
@app.route("/admin")
def admin_panel():    
    return render_template('admin/painel.html')

# Rota para listar categorias
@app.route("/admin/listar_categorias")
def listar_categorias():
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categorias').fetchall()
    conn.close()
    return render_template('admin/listar_categorias.html', categorias=categorias)


@app.route("/admin/cadastrar_categorias", methods=['GET', 'POST'])
def cadastrar_categorias():
    if request.method == 'POST':
        nome_categoria = request.form.get('nome_categoria')
        descricao = request.form.get('descricao')
        imagem = request.files.get('imagem')  # Obtém o arquivo de imagem enviado

        if nome_categoria:
            conn = get_db_connection()

            if imagem:  # Se uma imagem foi enviada
                imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
                conn.execute('INSERT INTO categorias (nome, descricao, imagem) VALUES (?, ?, ?)',
                             (nome_categoria, descricao, imagem_base64))
            else:
                conn.execute('INSERT INTO categorias (nome, descricao) VALUES (?, ?)',
                             (nome_categoria, descricao))

            conn.commit()
            conn.close()
            return redirect(url_for('listar_categorias'))

    return render_template('admin/cadastrar_categorias.html')


# Rota para excluir categoria
@app.route("/admin/excluir_categoria/<int:id>", methods=['GET', 'POST'])
def excluir_categoria(id):
    conn = get_db_connection()
    categoria = conn.execute('SELECT * FROM categorias WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        conn.execute('DELETE FROM categorias WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_categorias'))
    
    conn.close()
    return render_template('admin/excluir_categoria.html', categoria=categoria)


@app.route("/admin/editar_categoria/<int:id>", methods=['GET', 'POST'])
def editar_categoria(id):
    conn = get_db_connection()
    categoria = conn.execute('SELECT * FROM categorias WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nome_categoria = request.form.get('nome_categoria')
        descricao = request.form.get('descricao')
        nova_imagem = request.files.get('nova_imagem')

        if nome_categoria:
            if nova_imagem:  # Se uma nova imagem foi enviada
                nova_imagem_base64 = base64.b64encode(nova_imagem.read()).decode('utf-8')
                conn.execute('UPDATE categorias SET nome=?, descricao=?, imagem=? WHERE id=?', 
                             (nome_categoria, descricao, nova_imagem_base64, id,))
            else:
                conn.execute('UPDATE categorias SET nome=?, descricao=? WHERE id=?', 
                             (nome_categoria, descricao, id,))
                
            conn.commit()
            conn.close()
            return redirect(url_for('listar_categorias'))
    
    conn.close()
    return render_template('admin/editar_categoria.html', categoria=categoria)

@app.route("/admin/listar_pratos")
def listar_pratos():
    conn = sqlite3.connect('database\sqlite.db')
    conn.row_factory = sqlite3.Row
    pratos = conn.execute('SELECT * FROM pratos').fetchall()
    conn.close()
    return render_template('admin/listar_pratos.html', pratos=pratos)

@app.route("/admin/cadastrar_prato", methods=['GET', 'POST'])
def cadastrar_prato():
    if request.method == 'POST':
        nome_prato = request.form.get('nome_prato')
        descricao = request.form.get('descricao')
        categoria_id = request.form.get('categoria_id')
        imagem = request.files.get('imagem')  # Adicione esta linha para obter a imagem

        if nome_prato:
            conn = get_db_connection()

            if imagem:
                imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
                conn.execute('INSERT INTO pratos (nome, descricao, categoria_id, imagem) VALUES (?, ?, ?, ?)',
                             (nome_prato, descricao, categoria_id, imagem_base64))
            else:
                conn.execute('INSERT INTO pratos (nome, descricao, categoria_id) VALUES (?, ?, ?)',
                             (nome_prato, descricao, categoria_id))

            conn.commit()
            conn.close()
            return redirect(url_for('listar_pratos'))

    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categorias').fetchall()
    conn.close()
    return render_template('admin/cadastrar_prato.html', categorias=categorias)

@app.route("/admin/editar_prato/<int:id>", methods=['GET', 'POST'])
def editar_prato(id):
    conn = get_db_connection()
    prato = conn.execute('SELECT * FROM pratos WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nome_prato = request.form.get('nome_prato')
        descricao = request.form.get('descricao')
        categoria_id = request.form.get('categoria_id')
        nova_imagem = request.files.get('nova_imagem')  # Adicione esta linha para obter a nova imagem

        if nome_prato:
            if nova_imagem:
                nova_imagem_base64 = base64.b64encode(nova_imagem.read()).decode('utf-8')
                conn.execute('UPDATE pratos SET nome=?, descricao=?, categoria_id=?, imagem=? WHERE id=?', 
                             (nome_prato, descricao, categoria_id, nova_imagem_base64, id,))
            else:
                conn.execute('UPDATE pratos SET nome=?, descricao=?, categoria_id=? WHERE id=?', 
                             (nome_prato, descricao, categoria_id, id,))
                
            conn.commit()
            conn.close()
            return redirect(url_for('listar_pratos'))
    
    conn.close()
    categorias = get_db_connection().execute('SELECT * FROM categorias').fetchall()
    return render_template('admin/editar_prato.html', prato=prato, categorias=categorias)


# Rota para excluir prato
@app.route("/admin/excluir_prato/<int:id>", methods=['GET', 'POST'])
def excluir_prato(id):
    conn = get_db_connection()
    prato = conn.execute('SELECT * FROM pratos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM pratos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pratos'))

    conn.close()
    return render_template('admin/excluir_prato.html', prato=prato)

@app.route("/categoria/<int:categoria_id>")
def pratos_categoria(categoria_id):
    conn = get_db_connection()

    # Obtenha informações sobre a categoria
    categoria = conn.execute('SELECT * FROM categorias WHERE id = ?', (categoria_id,)).fetchone()

    # Obtenha todos os pratos dessa categoria
    pratos = conn.execute('SELECT * FROM pratos WHERE categoria_id = ?', (categoria_id,)).fetchall()

    conn.close()

    return render_template('pratos_categoria.html', categoria=categoria, pratos=pratos)

# cria a rota index
@app.route("/")
def index():
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categorias').fetchall()
    pratos = conn.execute('SELECT * FROM pratos').fetchall()
    conn.close()
    return render_template('index.html', categorias=categorias, pratos=pratos)

app.run(debug=True)