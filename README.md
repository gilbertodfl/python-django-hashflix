## Hashflix – Catálogo de Filmes em Django (Deploy na Railway)

Este projeto é um **aplicativo Django** chamado `hashflix`, com um app principal `filme`, que funciona como um catálogo de filmes (lista, detalhes, destaques, etc.), usando **Django 6.0.2**.

Em desenvolvimento local o banco padrão é **SQLite**, e em produção na **Railway** é usado **PostgreSQL** via `DATABASE_URL`.

### Tecnologias e versões principais

- **Linguagem**: Python 3.12+
- **Framework web**: Django 6.0.2
- **Banco de dados (desenvolvimento)**: SQLite (`db.sqlite3`)
- **Banco de dados (produção)**: PostgreSQL (via `dj-database-url` + `DATABASE_URL`)
- **Servidor WSGI em produção**: Gunicorn
- **Serviço de arquivos estáticos em produção**: Whitenoise
- **Formulários**: `django-crispy-forms` + `crispy-bootstrap5`
- **Outros pacotes**: `pillow`, `psycopg2`, `asgiref`, `sqlparse`, etc. (ver `requirements.txt`)
- **Gerenciamento de dependências**: `pip` + ambiente virtual (`venv`)

> As dependências já estão listadas em `requirements.txt`.

---

## Estrutura do projeto (resumo)

- `hashflix/` – configuração principal do projeto Django (`settings.py`, `urls.py`, `wsgi.py`).
- `filme/` – app responsável pelos filmes (models, views, urls, templates específicos).
- `templates/` – templates globais do projeto (por exemplo: `navbar.html`).
- `filme/templates/` – templates específicos do app `filme` (`homefilmes.html`, `detalhesfilme.html`).
- `static/` – arquivos estáticos (CSS, JS, imagens) configurados via `STATICFILES_DIRS`.
- `media/` – arquivos enviados pelo usuário (configurados via `MEDIA_URL` e `MEDIA_ROOT`).

---

## Requisitos

- **Python** 3.12 (ou versão compatível com Django 6.0.2)
- **pip** atualizado
- Opcional, mas recomendado: **virtualenv** (ou uso do módulo `venv` do Python)

Pacotes Python principais (ver `requirements.txt`):

- `Django==6.0.2`
- `gunicorn`, `dj-database-url`, `whitenoise`
- `django-crispy-forms`, `crispy-bootstrap5`, `django-bootstrap5`
- `psycopg2`, `pillow`, `asgiref`, `sqlparse`

Você pode instalar tudo de uma vez com:

```bash
pip install -r requirements.txt
```

---

## Configuração do ambiente (boa prática recomendada)

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd "python impressionador/django"
```

> Ajuste o caminho acima conforme a pasta em que você clonou o repositório.

### 2. Criar e ativar o ambiente virtual

Em **Linux / macOS**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Em **Windows (PowerShell)**:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

Se já existir um `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Se você adicionar novas dependências, gere novamente o `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Configuração do Django

### Variáveis de ambiente e segurança

O arquivo `hashflix/settings.py` está configurado para ler variáveis de ambiente em produção:

- `SECRET_KEY`: lida da variável `TOKEN_CSRF` (com uma chave de desenvolvimento como fallback).
- `DEBUG`: controlado por `PRODUCTION_DEBUG` (string `"True"` para ligar; qualquer outra coisa desliga).
- `ALLOWED_HOSTS`: já inclui o domínio da aplicação na Railway e `localhost/127.0.0.1`.
- `CSRF_TRUSTED_ORIGINS`: inclui a URL da aplicação na Railway.
- `DATABASE_URL`: quando definido, substitui o SQLite e passa a usar PostgreSQL via `dj-database-url`.

**Boas práticas para produção:**

- Não exponha a `SECRET_KEY` real no código; use sempre a variável `TOKEN_CSRF`.
- Mantenha `PRODUCTION_DEBUG` **sem ser "True"** em produção (ou simplesmente não defina a variável).
- Garanta que seu domínio esteja em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

### Banco de dados

Por padrão (desenvolvimento local):

- Engine: `django.db.backends.sqlite3`
- Arquivo: `db.sqlite3` na raiz do projeto.

Em produção (Railway), quando `DATABASE_URL` está definido:

- O projeto passa a usar **PostgreSQL** (ou outro banco apontado por essa URL).
- A configuração é feita automaticamente por `dj-database-url.config`.

### Templates e context processors

Em `hashflix/settings.py`, o projeto define:

- Diretório global de templates: `DIRS = ['templates']`
- App `filme` possui templates próprios (ex.: `homefilmes.html`, `detalhesfilme.html`).
- **Context processors** personalizados:
  - `filme.novos_context.lista_filmes_recentes`
  - `filme.novos_context.lista_filmes_emalta`
  - `filme.novos_context.filme_destaque`

Essas funções recebem `request` como primeiro parâmetro e retornam dicionários com listas/destaques de filmes, disponibilizando dados em todos os templates.

O template base `templates/base.html`:

- Carrega estáticos com `{% load static %}`.
- Define o favicon com `<link rel="icon" href="{% static 'favicon.ico' %}">`.
- Espera encontrar o arquivo `static/favicon.ico` (que será servido pelo Django/Whitenoise).

---

## Como rodar o projeto localmente

1. Certifique-se de que está com o ambiente virtual **ativado**.
2. Aplique as migrações:

```bash
python manage.py migrate
```

3. (Opcional) Crie um superusuário para acessar o admin:

```bash
python manage.py createsuperuser
```

4. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

5. Acesse no navegador:

- Aplicação: `http://127.0.0.1:8000/`
- Listagem de filmes (conforme suas URLs): por exemplo `http://127.0.0.1:8000/filmes/`
- Admin Django: `http://127.0.0.1:8000/admin/`

---

## Usuário personalizado e criação automática de admin

O projeto usa um **modelo de usuário personalizado**:

- `AUTH_USER_MODEL = 'filme.Usuario'`
- Classe `Usuario` herda de `AbstractUser` e adiciona o relacionamento `filmes_vistos` com `Filme`.

Para facilitar a criação do usuário administrador em produção (e também em desenvolvimento), existe um **comando de gestão**:

```bash
python manage.py cria_admin_automatico
```

Este comando:

- Lê as variáveis de ambiente `EMAIL_ADMIN` e `SENHA_ADMIN`.
- Se já existir um usuário com esse e-mail, não faz nada.
- Caso contrário, cria um superusuário com:
  - `username="admin"`
  - `email=EMAIL_ADMIN`
  - `password=SENHA_ADMIN`

Exemplo de uso local (Linux/macOS):

```bash
EMAIL_ADMIN=seu_email@example.com SENHA_ADMIN=suasenha python manage.py cria_admin_automatico
```

> Em produção (Railway), esse comando é executado automaticamente via `Procfile`, conforme descrito abaixo.

---

## Boas práticas recomendadas (nível sênior)

- **Separar configurações por ambiente**: por exemplo, `settings_dev.py`, `settings_prod.py`, ou uso de variáveis de ambiente para DEBUG, banco, credenciais, etc.
- **Nunca versionar dados sensíveis**: `SECRET_KEY`, senhas de banco, tokens de API devem vir de variáveis de ambiente.
- **Usar `requirements.txt` ou `pyproject.toml`**: facilita o deploy e garante reprodutibilidade do ambiente.
- **Usar migrations de forma controlada**: sempre rodar `makemigrations` e `migrate` em dev antes de subir para produção.
- **Organizar templates e estáticos**:
  - Templates globais na pasta `templates/` (layouts, navbar, base.html, etc.).
  - Templates específicos dos apps em `app/templates/app/*.html`.
  - Arquivos estáticos em `static/` (e `STATICFILES_DIRS`/`STATIC_ROOT` bem definidos).
- **Tratar internacionalização**: o projeto já está com `LANGUAGE_CODE = "pt-br"` e `TIME_ZONE = "America/Sao_Paulo"`. Se necessário, usar `ugettext_lazy` para textos traduzíveis.
- **Testes automatizados**: criar testes em `filme/tests.py` e usar `pytest` ou `python manage.py test` para garantir que views, models e context processors se comportam como esperado.

---

## Gerar um requirements.txt atualizado

Depois de instalar tudo que você precisa no ambiente virtual:

```bash
pip freeze > requirements.txt
```

Inclua este arquivo no versionamento (`git add requirements.txt`) para que qualquer pessoa possa reproduzir o ambiente.

---

## Deploy na Railway

Este projeto está preparado para ser deployado na **Railway** usando:

- `Procfile`
- `runtime.txt` (definindo a versão do Python)
- Variáveis de ambiente para banco, chave secreta e usuário admin.

### Procfile

O `Procfile` está configurado assim:

```text
web: python manage.py migrate && python manage.py cria_admin_automatico && gunicorn hashflix.wsgi --log-file -
```

Ordem das etapas:

1. `python manage.py migrate` – aplica migrações no banco (incluindo o modelo de usuário personalizado `Usuario`).
2. `python manage.py cria_admin_automatico` – garante que exista um superusuário com o e-mail definido nas variáveis de ambiente.
3. `gunicorn hashflix.wsgi` – sobe o servidor WSGI em produção.

### Variáveis de ambiente importantes na Railway

Configure pelo menos:

- `DATABASE_URL` – URL do banco (PostgreSQL da Railway).
- `TOKEN_CSRF` – valor usado como `SECRET_KEY` em produção.
- `PRODUCTION_DEBUG` – normalmente **não definir** ou deixar diferente de `"True"` para manter `DEBUG=False`.
- `EMAIL_ADMIN` – e-mail do usuário admin criado automaticamente.
- `SENHA_ADMIN` – senha do usuário admin criado automaticamente.

Além disso, o domínio gerado pela Railway deve estar:

- Em `ALLOWED_HOSTS`.
- Em `CSRF_TRUSTED_ORIGINS`.

---

## Próximos passos sugeridos

- Configurar **arquivos de configuração separados** para desenvolvimento/produção.
- Adicionar **testes unitários** para views e models do app `filme`.
- Documentar as principais **URLs** e **views** (por exemplo, página inicial, detalhes do filme, busca, etc.).
- Integrar ferramentas de qualidade de código, como **flake8**, **black** e **isort**, para manter o padrão do código consistente.

