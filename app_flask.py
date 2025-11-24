from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db
import requests  # Para integração opcional com FastAPI

app = Flask(__name__)
app.secret_key = 'chave_secreta_biblioteca'  # Necessário para flash messages

# Configuração para integração com FastAPI (opcional)
FASTAPI_URL = "http://localhost:8000"

@app.route('/')
def index():
    """
    Rota principal que exibe a lista de livros cadastrados
    Método HTTP: GET
    """
    try:
        # Busca todos os livros no banco de dados
        livros = db.listar_livros()
        return render_template('index.html', livros=livros)
    except Exception as e:
        flash(f'Erro ao carregar livros: {str(e)}', 'error')
        return render_template('index.html', livros=[])

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    """
    Rota para adicionar novos livros
    Métodos HTTP: GET (exibe formulário) e POST (processa dados)
    """
    if request.method == 'POST':
        try:
            # Obtém dados do formulário
            titulo = request.form.get('titulo', '').strip()
            autor = request.form.get('autor', '').strip()
            ano_publicacao = request.form.get('ano_publicacao', '').strip()
            
            # Validação básica dos dados
            if not titulo or not autor or not ano_publicacao:
                flash('Todos os campos são obrigatórios!', 'error')
                return redirect(url_for('adicionar_livro'))
            
            # Converte ano para inteiro
            try:
                ano_publicacao = int(ano_publicacao)
            except ValueError:
                flash('Ano de publicação deve ser um número válido!', 'error')
                return redirect(url_for('adicionar_livro'))
            
            # Insere no banco de dados
            db.criar_livro(titulo, autor, ano_publicacao, True)
            
            flash('Livro cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Erro ao cadastrar livro: {str(e)}', 'error')
            return redirect(url_for('adicionar_livro'))
    
    # GET: Exibe o formulário
    return render_template('adicionar.html')

@app.route('/editar/<int:livro_id>', methods=['GET', 'POST'])
def editar_livro(livro_id):
    """
    Rota para editar livros existentes
    """
    livro = db.buscar_livro_por_id(livro_id)
    if not livro:
        flash('Livro não encontrado!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            titulo = request.form.get('titulo', '').strip()
            autor = request.form.get('autor', '').strip()
            ano_publicacao = request.form.get('ano_publicacao', '').strip()
            disponivel = 'disponivel' in request.form
            
            if not titulo or not autor or not ano_publicacao:
                flash('Todos os campos são obrigatórios!', 'error')
                return redirect(url_for('editar_livro', livro_id=livro_id))
            
            try:
                ano_publicacao = int(ano_publicacao)
            except ValueError:
                flash('Ano de publicação deve ser um número válido!', 'error')
                return redirect(url_for('editar_livro', livro_id=livro_id))
            
            db.atualizar_livro(livro_id, titulo, autor, ano_publicacao, disponivel)
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Erro ao atualizar livro: {str(e)}', 'error')
            return redirect(url_for('editar_livro', livro_id=livro_id))
    
    return render_template('editar.html', livro=livro)

@app.route('/excluir/<int:livro_id>')
def excluir_livro(livro_id):
    """
    Rota para excluir livros
    Método HTTP: GET
    """
    try:
        if db.excluir_livro(livro_id):
            flash('Livro excluído com sucesso!', 'success')
        else:
            flash('Livro não encontrado!', 'error')
    except Exception as e:
        flash(f'Erro ao excluir livro: {str(e)}', 'error')
    
    return redirect(url_for('index'))

# Integração opcional com FastAPI
@app.route('/api/livros')
def listar_livros_api():
    """
    Endpoint que consome a API FastAPI (opcional)
    Demonstra integração entre Flask e FastAPI
    """
    try:
        response = requests.get(f"{FASTAPI_URL}/livros")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Erro ao buscar livros na API"}), 500
    except requests.exceptions.RequestException:
        return jsonify({"error": "FastAPI não está disponível"}), 503

if __name__ == '__main__':
    app.run(debug=True, port=5000)
