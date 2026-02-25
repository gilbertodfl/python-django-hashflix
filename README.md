## Hashflix – Projeto Django de Catálogo de Filmes

Este projeto é um **aplicativo Django** chamado `hashflix`, com um app principal `filme`, que funciona como um catálogo de filmes (lista, detalhes, destaques, etc.), usando **Django 6.0.2** e **SQLite** como banco padrão.

### Tecnologias e versões principais

- **Linguagem**: Python 3.12+
- **Framework web**: Django 6.0.2
- **Banco de dados (default)**: SQLite (arquivo `db.sqlite3`)
- **Gerenciamento de dependências**: `pip` + ambiente virtual (`venv`)

> Caso você ainda não tenha um arquivo de dependências (`requirements.txt`), veja a seção “Gerar requirements.txt” abaixo.

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

Pacotes Python mínimos:

- `Django==6.0.2`

Dependendo de recursos adicionais que você vier a adicionar (por exemplo, biblioteca de imagens, autenticação social, etc.), outros pacotes podem ser necessários.

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

Se ainda **não existir** `requirements.txt`, instale pelo menos o Django:

```bash
pip install --upgrade pip
pip install "Django==6.0.2"
```

Depois, gere o `requirements.txt` (boa prática):

```bash
pip freeze > requirements.txt
```

---

## Configuração do Django

### Variáveis de ambiente e segurança

O arquivo `hashflix/settings.py` atualmente está com:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `SECRET_KEY` exposto diretamente no código.

**Boas práticas para produção:**

- Nunca faça commit da `SECRET_KEY` real; use variáveis de ambiente (por exemplo, com `python-dotenv` ou `django-environ`).
- Defina `DEBUG = False` em produção.
- Preencha `ALLOWED_HOSTS` com os domínios/IPs em que o projeto será servido.

### Banco de dados

Por padrão:

- Engine: `django.db.backends.sqlite3`
- Arquivo: `db.sqlite3` na raiz do projeto.

Para ambiente de produção, é recomendável usar um banco mais robusto (PostgreSQL, MySQL, etc.) e configurar as credenciais por variáveis de ambiente.

### Templates e context processors

Em `hashflix/settings.py`, o projeto define:

- Diretório global de templates: `DIRS = ['templates']`
- App `filme` possui templates próprios (ex.: `homefilmes.html`, `detalhesfilme.html`).
- Dois **context processors** personalizados:
  - `filme.novos_context.lista_filmes_recentes`
  - `filme.novos_context.lista_filmes_emalta`

Essas funções recebem `request` como primeiro parâmetro e retornam dicionários com listas de filmes, disponibilizando dados em todos os templates.

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

## Próximos passos sugeridos

- Configurar **arquivos de configuração separados** para desenvolvimento/produção.
- Adicionar **testes unitários** para views e models do app `filme`.
- Documentar as principais **URLs** e **views** (por exemplo, página inicial, detalhes do filme, busca, etc.).
- Integrar ferramentas de qualidade de código, como **flake8**, **black** e **isort**, para manter o padrão do código consistente.

