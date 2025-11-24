from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from database import db
import uvicorn

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API Biblioteca Universitária",
    description="API REST para gerenciamento de livros da biblioteca universitária",
    version="1.0.0"
)

# Modelo Pydantic para validação de dados
class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200, description="Título do livro")
    autor: str = Field(..., min_length=1, max_length=100, description="Nome do autor")
    ano_publicacao: int = Field(..., ge=1000, le=2024, description="Ano de publicação")
    disponivel: bool = Field(default=True, description="Disponibilidade do livro")
    
    @validator('titulo', 'autor')
    def campos_nao_vazios(cls, v):
        """Valida se os campos não estão vazios após strip"""
        if not v.strip():
            raise ValueError('Campo não pode ser vazio')
        return v.strip()

class LivroCreate(LivroBase):
    pass

class LivroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    autor: Optional[str] = Field(None, min_length=1, max_length=100)
    ano_publicacao: Optional[int] = Field(None, ge=1000, le=2024)
    disponivel: Optional[bool] = None
    
    @validator('titulo', 'autor')
    def campos_nao_vazios(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Campo não pode ser vazio')
        return v.strip() if v else v

class LivroResponse(LivroBase):
    id: int
    
    class Config:
        orm_mode = True

@app.get("/")
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "message": "Bem-vindo à API da Biblioteca Universitária",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/livros", response_model=List[LivroResponse])
async def listar_livros():
    """
    Lista todos os livros cadastrados
    - **Método HTTP**: GET
    - **Código de Sucesso**: 200 OK
    """
    try:
        livros = db.listar_livros()
        return livros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@app.get("/livros/{livro_id}", response_model=LivroResponse)
async def buscar_livro(livro_id: int):
    """
    Busca um livro específico pelo ID
    - **Método HTTP**: GET
    - **Parâmetro Path**: livro_id (ID do livro)
    - **Código de Sucesso**: 200 OK
    - **Código de Erro**: 404 Not Found (livro não encontrado)
    """
    livro = db.buscar_livro_por_id(livro_id)
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado"
        )
    return livro

@app.post("/livros", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
async def criar_livro(livro: LivroCreate):
    """
    Cria um novo livro no sistema
    - **Método HTTP**: POST
    - **Body**: Dados do livro (JSON)
    - **Código de Sucesso**: 201 Created
    - **Código de Erro**: 400 Bad Request (dados inválidos)
    """
    try:
        # Validação adicional
        if not livro.titulo.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Título do livro é obrigatório"
            )
        
        # Insere no banco de dados
        livro_id = db.criar_livro(
            titulo=livro.titulo,
            autor=livro.autor,
            ano_publicacao=livro.ano_publicacao,
            disponivel=livro.disponivel
        )
        
        # Retorna o livro criado
        livro_criado = db.buscar_livro_por_id(livro_id)
        return livro_criado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar livro: {str(e)}"
        )

@app.put("/livros/{livro_id}", response_model=LivroResponse)
async def atualizar_livro(livro_id: int, livro_update: LivroUpdate):
    """
    Atualiza um livro existente
    - **Método HTTP**: PUT
    - **Parâmetro Path**: livro_id (ID do livro)
    - **Body**: Dados atualizados do livro (JSON)
    - **Código de Sucesso**: 200 OK
    - **Código de Erro**: 404 Not Found (livro não encontrado)
    """
    # Verifica se o livro existe
    livro_existente = db.buscar_livro_por_id(livro_id)
    if not livro_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado"
        )
    
    try:
        # Prepara os dados para atualização
        dados_atualizados = {
            'titulo': livro_update.titulo or livro_existente['titulo'],
            'autor': livro_update.autor or livro_existente['autor'],
            'ano_publicacao': livro_update.ano_publicacao or livro_existente['ano_publicacao'],
            'disponivel': livro_update.disponivel if livro_update.disponivel is not None else livro_existente['disponivel']
        }
        
        # Atualiza no banco de dados
        sucesso = db.atualizar_livro(
            livro_id=livro_id,
            titulo=dados_atualizados['titulo'],
            autor=dados_atualizados['autor'],
            ano_publicacao=dados_atualizados['ano_publicacao'],
            disponivel=dados_atualizados['disponivel']
        )
        
        if sucesso:
            livro_atualizado = db.buscar_livro_por_id(livro_id)
            return livro_atualizado
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar livro"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar livro: {str(e)}"
        )

@app.delete("/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_livro(livro_id: int):
    """
    Exclui um livro do sistema
    - **Método HTTP**: DELETE
    - **Parâmetro Path**: livro_id (ID do livro)
    - **Código de Sucesso**: 204 No Content
    - **Código de Erro**: 404 Not Found (livro não encontrado)
    """
    # Verifica se o livro existe
    livro = db.buscar_livro_por_id(livro_id)
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado"
        )
    
    try:
        sucesso = db.excluir_livro(livro_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao excluir livro"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir livro: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "api_fast:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload para desenvolvimento
    )
