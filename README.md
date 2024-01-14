# apagar


## TODO

- [x] salvar resultado
- [x] salvar resultado revisando prox. game/level
- [x] mvp frontend para visualizar resultados
- [x] escrever mais testes
- [ ] tipar os tipos parametros, ex. tournament_id esta string
- [x] listar top 4
- [x] doc inicial
- [ ] Poetry
- [ ] Deploy Fly.io
- [ ] Adicionar o output da solucao 1
- [ ] melhorar listar matches
- [ ] caso de marcar torneio como completo
- [ ] listar tournament
- [x] remover accounts
- [ ] adicionar estado tournament



## Próximos passos
- [✅] Terminar API de resultado
- [✅] Código retorno 400, 201 para criação
- [✅] Revisar se precisa ter um jogo a mais para definir 3o e 4o lugar
- [✅] Número de competidores impar passam para próxima rodada
- [✅] Fazer testes dos fluxos alternativos
- [  ] Teste final com 17 jogadores
- [  ] Criar documentação
- [  ] Revisar/Melhorar organização do projeto/código
- [  ] Limpar projeto
- [  ] Bug 6 jogadores que na fase dois temos numero impar de competidores
- [  ] Nao permitir incluir novos competidores qdo tem matches (inicializado)
- [  ] Testar com docker e postgres
- [  ] Deploy Fly.io

tour = Tournament.objects.all().first()

player = 'Alex Eala|Diana Shnaider|Polina Kudermetova|Kristina Dmitruk|Germany Mara Guth|John Doe|Oliva Galvones|Player One|Player Two|Rafael Nadal|Roger Federer|Leo Borg|Bruno Kuzuhara|Daniel Aguilar|Ethan Quinn|Tarantino'.split('|')

for name in players:
    tournaments_svc.create_competitor(tour.id, name)





# Desafio Mata-Mata

Bem-vindo a documentação da solução feita em Janeiro 2024 por Roger Camargo.
Espero que gostem! Ficarei feliz em responder qualquer pergunta!

- Fonte: TODO: adicionar link repo

## Funcionalidades

- [✅] Cadastro de novos torneios  ([POST] /tournament)
- [✅] Cadastro dos competidores   ([POST] /tournament/<id>/competitor)
- [✅] Listar competidores💡       ([GET]  /tournament/<id>/competitor)
- [✅] Listagem de partidas🚨      ([GET]  /tournament/<id>/match)
- [✅] Iniciar torneio💡🚨         ([POST] /tournament/<id>/start)         
- [✅] Salvar resultado partidas🚨 ([POST] /tournament/<id>/match/<id>)
- [✅] Exibição do TOP4            ([GET]  /tournament/<id>/result)

Legenda:
- 💡 Fora da listagem minima do desafio
- 🚨 Por onde comecei

## Como resolvi

- ✅ #1 Uma versão inicial fora de frameworks & API
- ❌ #2 Tentei utilizar meu [template Flask API](github.com/huogerac/cookiecutter-flask-openapi) como fundacao
- ❌ #3 Tentei comecar um projeto FastAPI do Zero
- ✅ #4 Comecei tudo de novo com Django (Calma! pode ser melhor que parece)

Notas:
- No repositorio, tem a pasta .vscode com os plugins

## ✅ #1 Solução sem framework, pensando na lógica do jogo apenas...

Dado um campeonato com 8 jogadores, conseguimos montar uma árvore de jogos até a final que define o campeão

```mermaid
flowchart TB
    p1--> 7:p1
    p2--> 7:p1
    p3--> 6:p3
    p4--> 6:p3
    p5--> 5:p5
    p6--> 5:p5
    p7--> 4:p7
    p8--> 4:p7

    7:p1--> 3:p1
    6:p3--> 3:p1
    5:p5--> 2:p5
    4:p7--> 2:p5

    3:p1--> 1:p1
    2:p5--> 1:p1
```

Com uma solução bem inicial utilizando este conceito, conseguimos montar toda árvore de jogos:

```python
class Tree:

    def __init__(self, name=None, winner='?', player1:'Tree'=None, player2:'Tree'=None):
        self.name = name
        self.winner = winner
        self.player1 = player1
        self.player2 = player2

    def __iter__(self):
      """ percorre toda ávore com base noso nós """
        yield self.name
        if self.player1:
            yield from self.player1
        if self.player2:
            yield from self.player2

    def __str__(self):
        return f'{self.name}' or '?'

    def level_counter(self):
        level = 0
        for num in self:
            level += 1
        return level
```

Pensando no mundo real, uma fase é as inscrições dos competidores, depois temos a montagem dos jogos, onde não será mais possível cadastrar novos competidores.
Com isto, temos o método para iniciar o campeonato:

```python
def start_tournament(tournament_id, seed=42):
    tournament = get_tournament(tournament_id)
    competitors = tournament.get("competitors").copy()
    players = [f"p{p['id']}" for p in competitors]

    random.seed(seed)
    random.shuffle(players)

    game_count = len(players)-1
    games = []
    while players:
        next_game, players = players[:2], players[2:]
        p1, p2 = next_game
        p1 = Tree(name=p1)
        p2 = Tree(name=p2)

        new_game = Tree(name=f'G{game_count}', player1=p1, player2=p2)
        games.append(new_game)
        game_count -= 1

    while len(games) > 2:
        next_final, games = games[:2], games[2:]
        p1, p2 = next_final
        new_game = Tree(name=f'G{game_count}', player1=p1, player2=p2)
        game_count -= 1

    p1, p2 = games
    final = Tree(name=f'G{game_count}', player1=p1, player2=p2)
    return final
```

Com basicamente este conceito, é possível montar a ávore de jogos. É claro, neste momento ainda falta os casos alternativos, como um número impar de jogadores. Mas com o salvar os resultados, vamos conseguir listar os jogos e os finalistas...
Enfim, foi uma prova de conceito para sentir um caminho da solução!

## ❌ #2 Implementar uma API com Flask

Uma com o rascunho da solucao, utilizei um [template Flask que fiz](), desta forma conseguiria gastar pouco tempo pensando na organizao, e principalmente na documentacao da API, algo que acredito ser muito importante! o CONTRATO da api ajuda todos que direta ou indiretamente vao utiliza-la.

Minha ideia era focar na solução do problema primeiro, gerar valor implementando as principais funcionalidades do desafio ao invés de ficar configurando variáveis de ambiente para o teste, migrações, ORM etc...

```shell
.
├── wimbledon
│   ├── app.py                    👉 Entrypoint (create_app)
│   ├── exceptions.py
│   ├── 🧅 ext                    👉 Settings
│   │   ├── ⚙️ configuration.py
│   │   ├── ⚙️ api.py
│   │   └── ⚙️ database.py
│   │   ...
│   ├── 🧅 api                    👉 API Routes
│   │   ├── 📦 tournament.py
│   │   ├── 📦 users.py           [EXEMPLO]
│   │   └── 📦 openapi.yaml       👉 API Contract
│   │   ...
│   ├── 🧅 services               👉 Business rules
│   │   ├── 📦 tournament.py 🎂
│   │   ├── 📦 users.py 🎂
│   │   ...
│   └── 🧅 models                 👉 ORM
│       ├── 📦 tournament.py
│       └── 📦 users.py
```

- Postgres

PROBLEMA: Como já tem mais de 3 anos que não trabalho com Flask, este projeto não roda mais, Flask 1.1.4 conflita com SQLAlchemy. Mesmo com todas versões fixadas no requirements, não roda. Gastei horas tentando atualizar as bibliotecas e quando fiz rodar, a API do SQLAlchemy mudou um pouco. (ai um motivo para usar um Poetry/pip-tools)

ENFIM, parece que fazia mais sentido eu começar do zero ao invés de utilizar o template que esta bem quebrado!

COMEÇAR DO ZERO? Bom, já que vou ter que configurar .dotenv, ORM, Migrações etc...Bom, acredito que faz mais sentido ir para um FastAPI, ainda mais que estou meio desatualizado o que mudou no Flask 2 e 3.

## ❌ #3 Implementar do zero uma API com FastAPI

Iniciei fazendo um TODO list:
- Gerenciador de pacotes (Poetry)
- Criar um endpoint fora do app.py (mais organizado)
- Pytest
- .env
- Conexão com o banco
- Migrations
- CLI

PROBLEMA: Por mais que estava evoluindo rápido, estava fácil adicionar as coisas, documentação boa...já se passaram várias horas e NÃO ESTAVA FOCANDO no problema do campeonado! Parei um pouco a organização e comecei fazer a modelagem, tentei retornar as partidas, escrevendo alguns testes etc...
Mas estava gastando muito tempo para entender as mudanças no SQLAlchemy mais novo. Coisas simples como `Players.query.order_by(Players.id.desc()).all()` não funcionavam de primeira!

Dado que ainda estava faltando resolver problemas bem mais complexos, como a listagem dos 4 melhores, criar partidas com número impar de jogadores!
Meu tempo acabando e eu batendo cabeça com ORM e organização de projeto!

DECIDI começar do zero novamente usando coisas da minha zona de conforto! focar no domínio da solução ao invés da nova API do ORM.

Comecei com Django! CALMA! olhem com o olhar de investidor, acredito que o resultado foi melhor que eu esperava, em muito menos tempo as principais funcionalidades estavam prontas! com testes e pude resolver os casos alternativos utilizando TDD com zero esforco. 👇

## ✅ #4 Tudo do zero com Django utilizando o template Djàvue...

No começo deste ano contribui bastante para a versão 3 deste template, e achei que poderia utiliza-lo para me ajudar nesta entrega!

Este projeto segue a organização do Djàvue que pode ser [acessada aqui](https://github.com/evolutio/djavue3). Mais informações pode ser vista nesta documentação criada por mim mesmo aqui: [https://djavue.org/](https://www.djavue.org/README_EN.html)


## Fundação

- Gerenciador de pacotes
- dotenv para facilitar rodar em diferentes ambientes, escolher com ou sem Docker etc...
- API com documentacao automatica (swagger)
- Linter e formatador de codigo (Flake8 e Black)
- Pytest
- Docker para rodar tudo com 1 comando
- CI com GitHub Actions

## Domínio da solução

```mermaid
---
title: Entidades
---
classDiagram
    
    Match "*" <-- "1" Tournament
    Match --> "1" Competitor: Player 1
    Match --> "1" Competitor: Player 2
    class Tournament{
        -name
    }
    class Match{
        -game_number
        -game_extra
        -game_extra
    }
    class Competitor{
        -name
    }
```

## Iniciando - Rodando o projeto

## Requisitos

- Git
- 🐍 Python +3.9
- Um terminal (de preferencia um terminal Linux, é para funcionar em um terminal WSL no Windows)

Temos duas formas para **Rodar** escolha o sabor 🍨:
- Sem Docker 📦: Apenas **Python** (usando sqlite)
- Apenas Banco de dados usando 🐋 Docker
- Tudo usando Docker 🐋: **Docker** and **Docker compose**


## Rodar local (min.dependencias) sem Docker 🦄

🌈 TIPS/TRICKS: Melhor utilizar Python 3.10 ou mais novo. Uma boa forma de gerenciar versoes de python é utilizar ferramentas como [Pyenv](https://github.com/pyenv/pyenv) ou [asdf](https://github.com/asdf-vm/asdf) 

Clonar e entrar na pasta do projeto

```shell
git clone ...
cd wimbledon/
```

Vamos agora criar um ambiente virtual Python e instalar as dependencias:

⚠️ **warning**
Nao esqueca de ativar o ambiente (`source .venv/bin/activate`)

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

- **IMPORTANTE**:
Vamos precisar confirmar como que as variáveis de ambiente estão configuradas no arquivo `.env`. Temos que confirmar que as configurações para rodar local estão sem comentário:

```shell
DEBUG=True
SECRET_KEY='cria-um-segredo-qualquer'
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo

POSTGRES_DB=db_posts
POSTGRES_USER=posts
POSTGRES_PASSWORD=posts

# ⚠️ AVISO
# É possível alterar entre COM DOCKER ou SEM DOCKER conforme as configurações abaixo

## 🖥️  Para uso local via virtualenv
POSTGRES_HOST=localhost
POSTGRES_PORT=15432
DATABASE_URL=postgres://posts:posts@localhost:15432/db_posts
DATABASE_URL=sqlite:///db_local.sqlite3

## 🐳 Para uso via container/Docker
# POSTGRES_HOST=postgres
# POSTGRES_PORT=5432
# DATABASE_URL=postgres://posts:posts@postgres:5432/db_posts
```

Agora, vamos criar as migracoes, ou seja, as tabelas inicias do projeto (com base nas definicoes dos models). Note que o Django já vem com alguns problemas resolvidos, então vamos ter umas tabelas a mais, como usuário e sessões. Pode parecer estranho para este projeto, mas no mundo real, não queremos qualquer pessoa enviando resultado dos jogos, logo vamos precisar de autenticao. 

Nota: Neste momento, todos endpoints estão abertos, mas é bem fácil protegê-los

```shell
./manage.py migrate
```
Finalmente, podemos rodar o projeto:

```shell
./manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 13, 2024 - 16:59:18
Django version 4.1.7, using settings 'wimbledon.wimbledon.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

👉 Pode abrir seu navegador e acessar `http://localhost:8000`

**OPCIONAL**

Para acessar o back-office, podemos criar um usuário administrador e acessar a página Admin do Django

```shell
./manage.py createsuperuser

Usuário: admin
Endereço de email: admin@example.br
Password: **********
Password (again): **********
Superuser created successfully.
```

👉 Pode abrir seu navegador e acessar `http://localhost:8000/admin`

Outras coisas que podemos fazer neste ponto:

- Rodar o comando `pytest` e rodar todos os testes
- Rodar o comando `./manage.py shell_plus` ou `./manage.py shell_plus --print-sql` 
- Dentro shell rodar comandos como `Tournament.objects.all()` e `Tournament.objects.create(description='Meu novo torneio teste')`

Ou podemos Criar e iniciar um torneio com:

```python
from wimbledon.core.services import tournaments_svc

tourneio = Tournament.objects.create(description='Wimbledon 2024')
tourneio.save()

competidores = 'Alex|Diana|Polina|Kristina|Mara Guth|John Doe|Oliva||Rafael'.split('|')
[tournaments_svc.create_competitor(torneio.id, name) for name in players]

tournaments_svc.start_tournament(torneio.id)
tournaments_svc.list_matches(torneio.id)

```


## Rodar tudo com 🐋 (Usando Postgres)

**Requirements:**

- Docker version >= 24.0.2 (in any S.O. you have)
- Docker Compose version >= v2.18.1
- Um terminal ou WSL no Windows

Como a aplicação se comporta em tempo de execução é com base nas configurações do settings para um determinado ambiente seguindo o [12 factors](https://12factor.net/), desta forma, podemos conectar em um sqllite ou em Posgres, pode ser em modo DEBUG ou não. Estas configurações estão no arquivo .env

Para utilizar Docker, vamos comentar as linhas para uso com virtualenv e DESCOMENTAR as linhas para uso com Docker:

```shell
DEBUG=True
SECRET_KEY='cria-um-segredo-qualquer'
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo

POSTGRES_DB=db_posts
POSTGRES_USER=posts
POSTGRES_PASSWORD=posts

# ⚠️ AVISO
# É possível alterar entre COM DOCKER ou SEM DOCKER conforme as configurações abaixo

## 🖥️  Para uso local via virtualenv
#POSTGRES_HOST=localhost
#POSTGRES_PORT=15432
#DATABASE_URL=postgres://posts:posts@localhost:15432/db_posts
#DATABASE_URL=sqlite:///db_local.sqlite3

## 🐳 Para uso via container/Docker
 POSTGRES_HOST=postgres
 POSTGRES_PORT=5432
 DATABASE_URL=postgres://posts:posts@postgres:5432/db_posts
```

Primeiramente, independente de qual diretório você está, veja se já existe algum container iniciado. De preferência, tente parar ou apagar os containers e forma a deixar a lista vazia.

```shell
docker ps

CONTAINER ID   IMAGE  COMMAND      CREATED       STATUS                PORTS 
``` 

👉 **INFO**:
Se sua lista exibir algum container, você precisa fazaer um `docker stop [CONTAINER ID]`


Entre no diretório do projeto

```shell
cd wimbledon/
```

Digite o comando para iniciar os containers em modo "detached"

```shell
docker compose up -d
```

Depois de baixar as camadas e fazer o "build" das imagens, digite novamente o comando `docker ps`, ele deverá listar dois containers: o backend e o banco de dados postgres rodando:

```shell
docker ps

CONTAINER ID  IMAGE COMMAND                 STATUS         PORTS        NAMES
e5c00ed78     back-dashboard "bash -..."    Up 10 minutes  8000->8000   wimbledon-backend-1
3f0949de3     postgres:13.3 "docker..."     Up 10 minutes  15432->5432  wimbledon-postgres-1
```

Estes containers estão rodando conforme as configurações no arquivo `docker-compose.yaml`:

```YAML
services:

  backend:
    image: back-wimbledon
    hostname: back-wimbledon
    build:
      context: ./
      dockerfile: Dockerfile
    env_file:
      - .env
    ...

  postgres:
    image: "postgres:15-alpine"
    ports:
      - 15432:5432
    expose:
      - "15432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
    restart: on-failure
    ...
```

**DONE!! 🎉🎉** Os containers estão prontos para uso

👉 Abra seu navegador e acesse `http://localhost:8000`

Você pode acessar o container **backend container** e digita os mesmos comandos utilizados sem docker, primeiro é necessário entrar dentro do container:

```shell
docker compose exec -it backend bash
```

Uma vez dentro do container, podemos digitar os comandos do Django como mostrado na sessão anterior (Rodar sem docker)

Use `CTRL+D` ou digite `exit` para fechar o terminal de dentro do container docker e voltar para o terminal do host.

**Outras coisas que podemos fazer neste ponto:**
- Use `docker compose exec -it backend [command]` para executar qualquer comando dentro do container 
- Use `docker compose down` para parar todos os container
- Use `docker compose logs -f backend` para ver os logs do container. Nota: se o container não iniciar, este comando pode ajudar a entender por que o container não iniciou.


## Iniciando - Entendendo o projeto

## Arquitetura

```mermaid
classDiagram
    direction LR
    Cliente --> API: urls+views
    API --> Services : Regras
    API *-- Schemas
    Services --> ORM
    ORM *-- Models
```

- **Cliente**: Qualquer coisa que faz chamadas HTTP para a API
- **API**: Tem as definições de rotas e validação dos dados de entrada, sem ou pouca regras de negócio, redireciona os dados para a camada de serviço
- **Services**: Módulos python puro com a implementação das regras de negócio, é a camada que mais deve ser testada
- **ORM**: Mapeamento dos dados na base de dados


## Estrutura & Organizacao

```shell
Wimbledon
 ├── README.md
 ├── manage.py
 ├── requirements-dev.txt
 ├── requirements.txt
 ├── docker-compose.yml
 ├── Dockerfile
 ├── tox.ini
 ├── uwsgi.ini
 └── wimbledon                       👉 base do projeto
    ├── base                        👉 app comum
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   ├── tests
    │   ├── urls.py
    │   └── views.py
    ├── core                        👉 app inicial
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py               👉 ORM
    │   ├── service
    │   │   └── tournaments_svc.py  👉 REGRAS
    │   ├── tests
    │   ├── urls.py
    │   ├── schemas.py              👉 Validação input
    │   └── views.py                👉 ENDPOINTS
    └── wimbledon
        ├── api.py
        ├── settings.py             👉 CONFIGURAÇÕES
        ├── urls.py
        └── wsgi.py
```

