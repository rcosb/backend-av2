import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name='biblioteca.db'):
        self.db_name = db_name
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager para gerenciar conexões com o banco"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        """Inicializa o banco de dados criando a tabela se não existir"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER NOT NULL,
                    disponivel BOOLEAN DEFAULT TRUE
                )
            ''')
    
    def criar_livro(self, titulo, autor, ano_publicacao, disponivel=True):
        """Cria um novo livro no banco"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES (?, ?, ?, ?)',
                (titulo, autor, ano_publicacao, disponivel)
            )
            return cursor.lastrowid
    
    def listar_livros(self):
        """Lista todos os livros do banco"""
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM livros ORDER BY id DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def buscar_livro_por_id(self, livro_id):
        """Busca um livro específico pelo ID"""
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def atualizar_livro(self, livro_id, titulo, autor, ano_publicacao, disponivel):
        """Atualiza um livro existente"""
        with self.get_connection() as conn:
            conn.execute(
                'UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ? WHERE id = ?',
                (titulo, autor, ano_publicacao, disponivel, livro_id)
            )
            return conn.total_changes > 0
    
    def excluir_livro(self, livro_id):
        """Exclui um livro do banco"""
        with self.get_connection() as conn:
            conn.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
            return conn.total_changes > 0

# Instância global do banco de dados
db = Database()
