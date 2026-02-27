## Deploy do Hashflix na Railway

Este guia descreve **passo a passo** como publicar este projeto Django (`hashflix`) na **Railway**, usando PostgreSQL, `Procfile` e o comando de criação automática de admin.

> Tudo aqui foi escrito especificamente para **este repositório**.

---

## 1. Pré-requisitos

- Conta criada em [`railway.app`](https://railway.app).
- Repositório do projeto no GitHub (ou GitLab/Bitbucket) contendo:
  - `hashflix/`, `filme/`, `templates/`, `static/` etc.
  - `requirements.txt`
  - `runtime.txt`
  - `Procfile`
- Python local instalado (opcional, mas útil para testar antes).

---

## 2. Criar o projeto na Railway e conectar o repositório

1. Acesse o painel da Railway.
2. Clique em **"New Project"**.
3. Escolha **"Deploy from GitHub repo"**.
4. Conecte sua conta GitHub (se ainda não estiver conectada).
5. Selecione o repositório deste projeto (`hashflix`).
6. Confirme a criação do serviço.

A Railway vai:

- Detectar que é um projeto Python.
- Usar `runtime.txt` para definir a versão do Python.
- Usar o `Procfile` para saber como iniciar o serviço web.

---

## 3. Adicionar um banco de dados PostgreSQL

1. No projeto da Railway, clique em **"Add New"** ou **"New"**.
2. Escolha **"Database"** e selecione **PostgreSQL**.
3. Após a criação do banco, volte ao serviço web (o serviço que aponta para o seu repositório).
4. Clique em **"Variables"** (ou **"Environment"**).
5. Verifique se existe uma variável do tipo `DATABASE_URL` já disponibilizada pelo banco.
   - Em muitos casos, a Railway já injeta automaticamente `DATABASE_URL` quando você conecta o DB ao serviço.
   - Se não estiver aparecendo, copie a URL de conexão do banco e crie manualmente a variável:

   - **Nome**: `DATABASE_URL`  
   - **Valor**: URL de conexão (começando com `postgres://` ou `postgresql://`).

No projeto, o `hashflix/settings.py` está preparado para:

- Usar SQLite localmente (sem `DATABASE_URL`).
- Trocar automaticamente para PostgreSQL quando `DATABASE_URL` estiver definido.

---

## 4. Configurar variáveis de ambiente do Django

Ainda na aba de **Variables** do serviço web, configure:

### 4.1. Segurança e debug

- **`TOKEN_CSRF`**  
  - Valor: uma string longa e aleatória (pode ser um UUID, por exemplo).  
  - É usada como `SECRET_KEY` em produção.

- **`PRODUCTION_DEBUG`**  
  - Valor em produção: normalmente **deixe em branco** ou qualquer coisa **diferente de `"True"`**.  
  - Se você definir `PRODUCTION_DEBUG="True"`, o `DEBUG` do Django ficará ligado (não recomendado em produção).

### 4.2. Usuário admin automático

O projeto possui um comando de gestão `cria_admin_automatico`, usado no `Procfile`.  
Ele depende destas variáveis:

- **`EMAIL_ADMIN`**  
  - E-mail do superusuário que será criado automaticamente.

- **`SENHA_ADMIN`**  
  - Senha do superusuário criado automaticamente.

O comando:

```bash
python manage.py cria_admin_automatico
```

- Cria um superusuário com `username="admin"`, `email=EMAIL_ADMIN`, `password=SENHA_ADMIN`, caso ainda não exista um usuário com esse e-mail.
- Se o usuário já existir, **não faz nada** (idempotente).

### 4.3. Domínio / Hosts

No `settings.py`, já existem valores padrão em:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

Certifique-se de que o domínio gerado pela Railway (algo como `https://<nome>.up.railway.app`) esteja contemplado nessas listas.  
Se o domínio mudar, lembre-se de atualizar esses valores no código e fazer novo deploy.

---

## 5. Entendendo o Procfile

O `Procfile` deste projeto contém:

```text
web: python manage.py migrate && python manage.py cria_admin_automatico && gunicorn hashflix.wsgi --log-file -
```

Na prática, a Railway executa:

1. `python manage.py migrate`
   - Aplica todas as migrações no banco (incluindo o modelo de usuário personalizado `filme.Usuario`).
2. `python manage.py cria_admin_automatico`
   - Garante que exista um superusuário com `EMAIL_ADMIN`/`SENHA_ADMIN`.
3. `gunicorn hashflix.wsgi --log-file -`
   - Inicia o servidor WSGI para servir o Django em produção.

Você não precisa alterar esse comando para o uso básico; apenas garanta que as variáveis de ambiente estão corretas.

---

## 6. Arquivos estáticos e favicon

O projeto usa:

- `Whitenoise` para servir arquivos estáticos em produção.
- Uma pasta `static/` na raiz do projeto, configurada em `STATICFILES_DIRS`.
- Um favicon referenciado em `templates/base.html`:

```html
<link rel="icon" href="{% static 'favicon.ico' %}">
```

Para que o favicon funcione em produção:

1. Crie (ou mova) o arquivo `favicon.ico` para a pasta:

   ```text
   static/favicon.ico
   ```

2. Faça commit e push desse arquivo.
3. Deixe a Railway fazer um novo deploy.

Se o favicon estiver fora de `static/` (por exemplo, na raiz do projeto), a URL `/favicon.ico` poderá retornar `404` nos logs.

---

## 7. Disparar o primeiro deploy

Com o repositório conectado e as variáveis configuradas:

1. No painel da Railway, entre no serviço web.
2. Clique em **"Deploy"** (ou faça um push para a branch principal, se o deploy automático estiver habilitado).
3. Aguarde o build e a execução do comando do `Procfile`.

Você pode acompanhar o progresso em:

- Aba **"Deployments"** → logs do build.
- Aba **"Logs"** → saída do serviço web (inclui logs do Django e do Gunicorn).

No primeiro deploy, os logs devem mostrar:

- Migrações sendo aplicadas (`python manage.py migrate`).
- Mensagens do comando `cria_admin_automatico`.
- Mensagem do Gunicorn indicando que está escutando em um endereço/porta (por exemplo, `0.0.0.0:8080`).

---

## 8. Testar a aplicação em produção

1. No projeto da Railway, clique no serviço web.
2. Clique no botão de **"Open"** ou no link do domínio (ex.: `https://hashflix-production.up.railway.app`).
3. Verifique:
   - Página inicial abre sem erro.
   - Rotas como `/filmes/` funcionam.
   - Acesso ao admin em `/admin/` usando o e-mail/senha do `EMAIL_ADMIN` / `SENHA_ADMIN`.
   - Favicon aparece no navegador (ou, pelo menos, não há mais `Not Found: /favicon.ico` nos logs).

Se algo der errado:

- Verifique os **logs** na Railway.
- Confirme se as variáveis de ambiente estão corretamente definidas.
- Confirme se o banco de dados está acessível e se `DATABASE_URL` está correto.

---

## 9. Atualizações futuras

Quando fizer mudanças no código:

1. Faça commit e push na mesma branch monitorada pela Railway.
2. A Railway vai iniciar um novo deploy automático.
3. Novas migrações (se houver) serão aplicadas pelo `python manage.py migrate`.
4. O comando `cria_admin_automatico` vai rodar de novo, mas só criará o usuário admin se ele ainda não existir.

Assim, você mantém o fluxo de deploy **simples e repetível**, com o mínimo de configuração manual possível.

