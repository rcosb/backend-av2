# Sistema de Cadastro de Livros - Biblioteca Universitária

Sistema completo desenvolvido com Flask (interface web) e FastAPI (API REST) para gerenciamento de livros de uma biblioteca universitária.

## 📋 Requisitos

- Python 3.8+
- Dependências listadas no `requirements.txt`

## 🚀 Instalação e Execução

### 1. Clone o repositório ou baixe os arquivos

### 2. Instale as dependências

```bash

pip install -r requirements.txt

``` 

### 3. Execute a aplicação Flask (Porta 5000)

```bash

python app_flask.py

``` 

### 4. Execute a API FastAPI (Porta 8000)

Em outro terminal:

```bash

python api_fast.py

``` 

### 5. Acesse as aplicações

Flask (Interface Web): http://localhost:5000

FastAPI (Documentação): http://localhost:8000/docs

FastAPI (Redoc): http://localhost:8000/redoc

### 🗄️ Estrutura do Banco de Dados

O sistema utiliza SQLite com a tabela livros:

```txt
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
titulo (TEXT, NOT NULL)
autor (TEXT, NOT NULL)
ano_publicacao (INTEGER, NOT NULL)
disponivel (BOOLEAN, DEFAULT TRUE)
```

### 🔧 Funcionalidades
***Flask (Interface Web)***

✅ Listagem de livros

✅ Cadastro de novos livros

✅ Edição de livros existentes

✅ Exclusão de livros

✅ Interface responsiva com Bootstrap

***FastAPI (API REST)***

✅ GET /livros - Lista todos os livros

✅ GET /livros/{id} - Busca livro por ID

✅ POST /livros - Cria novo livro

✅ PUT /livros/{id} - Atualiza livro existente

✅ DELETE /livros/{id} - Exclui livro

✅ Validação de dados com Pydantic

✅ Documentação automática (Swagger/Redoc)

### 🧪 Testes
**Teste a interface web:**

Acesse http://localhost:5000

Adicione, edite e exclua livros

**Teste a API:**

Acesse http://localhost:8000/docs

Use a interface Swagger para testar os endpoints

Ou use ferramentas como curl, Postman, ou Insomnia

**Exemplo de requisições curl:**

***Listar livros:***

```bash

curl -X GET "http://localhost:8000/livros"

``` 

***Criar livro:***

``` bash

curl -X POST "http://localhost:8000/livros" \
     -H "Content-Type: application/json" \
     -d '{"titulo":"Dom Casmurro","autor":"Machado de Assis","ano_publicacao":1899,"disponivel":true}'

``` 

***Atualizar livro:***

``` bash

curl -X PUT "http://localhost:8000/livros/1" \
     -H "Content-Type: application/json" \
     -d '{"titulo":"Dom Casmurro - Edição Especial","disponivel":false}'

``` 

***Excluir livro:***

``` bash

curl -X DELETE "http://localhost:8000/livros/1"

``` 

### 📁 Estrutura de Arquivos

```text

biblioteca/
├── app_flask.py          # Aplicação Flask
├── api_fast.py           # API FastAPI
├── database.py           # Gerenciamento do banco de dados
├── requirements.txt      # Dependências do projeto
├── biblioteca.db         # Banco de dados SQLite (criado automaticamente)
└── templates/            # Templates HTML do Flask
    ├── base.html
    ├── index.html
    ├── adicionar.html
    └── editar.html

```

### 🔄 Códigos de Status HTTP Utilizados

200 OK - Requisição bem-sucedida

201 Created - Recurso criado com sucesso

204 No Content - Exclusão bem-sucedida

400 Bad Request - Dados inválidos

404 Not Found - Recurso não encontrado

500 Internal Server Error - Erro interno do servidor

### 🛠️ Tecnologias Utilizadas

- Backend: Flask, FastAPI
- Banco de Dados: SQLite
- Validação: Pydantic
- Frontend: HTML, Bootstrap, Jinja2
- Documentação: Swagger UI, ReDoc

**requirements.txt**

```txt

flask==2.3.3
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
requests==2.31.0

``` 
