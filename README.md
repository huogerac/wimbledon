# 🏆 Desafio Mata-Mata

Bem-vindo a documentação da solução feita em Janeiro 2024 por Roger Camargo.
Espero que gostem! Ficarei feliz em responder qualquer pergunta!

- Fonte: [https://github.com/huogerac/wimbledon](https://github.com/huogerac/wimbledon)
- API: [https://wimbledon.fly.dev/api/docs](https://wimbledon.fly.dev/api/docs)

## Funcionalidades

- [✅] Cadastro de novos torneios  ([POST] /tournament)
- [✅] Cadastro dos competidores   ([POST] /tournament/<id>/competitor)
- [✅] Listar competidores💡       ([GET]  /tournament/<id>/competitor)
- [✅] Listagem de partidas🚨      ([GET]  /tournament/<id>/match)
- [✅] Iniciar torneio💡🚨         ([POST] /tournament/<id>/start)         
- [✅] Salvar resultado partidas🚨 ([POST] /tournament/<id>/match/<id>)
- [✅] Exibição do TOP4            ([GET]  /tournament/<id>/result)

Legenda:
- 💡 Fora da listagem mínima do desafio
- 🚨 Por onde comecei


### 🎥 ** VÍDEO 1:** Apresentação da API e do funcionamento
- 👉 [https://www.loom.com/share/3ca2c06ba9d242a1b5f1d2a64276f504](https://www.loom.com/share/3ca2c06ba9d242a1b5f1d2a64276f504)


## Como resolvi

- ✅ #1 Uma versão inicial fora de frameworks & API
- ❌ #2 Tentei utilizar meu [template Flask API](github.com/huogerac/cookiecutter-flask-openapi) como fundacao
- ❌ #3 Tentei começar um projeto FastAPI do Zero
- ✅ #4 Comecei tudo de novo com Django (Calma! pode ser melhor que parece) 👈

Notas:
- No repositório, tem a pasta .vscode com os plugins


### 🎥 ** VÍDEO 2:** As etapas até chegar na solução
- 👉 [https://www.loom.com/share/b3e4dfdf4669464fb3a835bd0218d014](https://www.loom.com/share/b3e4dfdf4669464fb3a835bd0218d014)


## ✅ #1 Solução sem framework, pensando na lógica do jogo apenas...

Dado um campeonato com 8 jogadores, conseguimos montar uma árvore de jogos até a final que define o campeão

```mermaid
flowchart BT
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

Com uma solução bem inicial utilizando este conceito, conseguimos montar toda a árvore de jogos:

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

Com basicamente este conceito, é possível montar a árvore de jogos. É claro, neste momento ainda faltam os casos alternativos, como um número ímpar de jogadores. Mas com o salvar os resultados, vamos conseguir listar os jogos e os finalistas...
Enfim, foi uma prova de conceito para sentir o caminho da solução!

## ❌ #2 Implementar uma API com Flask

Uma vez com o rascunho da solução, utilizei o [template Flask que fiz](https://github.com/huogerac/cookiecutter-flask-openapi/), desta forma conseguiria gastar pouco tempo pensando na organização, e principalmente na documentação da API, algo que acredito ser muito importante! o CONTRATO da api ajuda todos que direta ou indiretamente vão utilizá-la.

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

[Post que fiz com relação a organização de projetos Flask](https://huogerac.hashnode.dev/estrutura-e-organizacao-de-pastas-em-projetos-flask)

Também estava pesquisando como utilizar o [`WITH RECURSIVE` do Postgres](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE) para tentar obter toda árvore dos jogos:

```SQL
WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

PROBLEMA: Como já tem mais de três anos que não trabalho com Flask, este projeto não roda mais, Flask 1.1.4 conflita com SQLAlchemy. Mesmo com todas as versões fixadas no requirements, não roda. Gastei horas tentando atualizar as bibliotecas e quando fiz rodar, a API do SQLAlchemy mudou um pouco. (um motivo para usar um Poetry/pip-tools)

ENFIM, parece que fazia mais sentido eu começar do zero ao invés de utilizar o template que está bem quebrado!

COMEÇAR DO ZERO? Bom, já que vou ter que configurar .dotenv, ORM, Migrações etc...Bom, acredito que faz mais sentido ir para um FastAPI, ainda mais que estou meio desatualizado com o que mudou no Flask 2 e 3.

## ❌ #3 Implementar do zero uma API com FastAPI

Iniciei fazendo um TODO list:
- Gerenciador de pacotes (Poetry)
- Criar um endpoint fora do app.py (mais organizado)
- Pytest
- .env
- Conexão com o banco
- Migrations
- CLI

PROBLEMA: Por mais que estivesse evoluindo rápido, estava fácil adicionar as coisas, documentação legal do FastAPI...já se passaram várias horas e NÃO ESTAVA FOCANDO no problema do campeonato! Parei um pouco a organização e comecei fazer a modelagem, tentei retornar as partidas, escrever alguns testes etc...
Mas estava gastando muito tempo para entender as mudanças no SQLAlchemy mais novo. Coisas simples como `Players.query.order_by(Players.id.desc()).all()` não funcionavam de primeira!

Dado que ainda estava faltando resolver problemas bem mais complexos, como a listagem dos 4 melhores, criar partidas com número ímpar de jogadores!
Meu tempo acabando e eu batendo cabeça com ORM e organização de projeto!

**TODO:** Enviar o que consegui fazer com FastAPI

👉 DECIDI então começar do zero novamente usando coisas da minha zona de conforto! focar no domínio da solução ao invés da nova API do ORM.

Comecei com Django! CALMA! olhem com o olhar de investidor, acredito que o resultado foi melhor que eu esperava, em muito menos tempo as principais funcionalidades estavam prontas! com testes e pude resolver os casos alternativos utilizando TDD com zero esforço de configuração. 👇


## ✅ #4 Tudo do zero com Django utilizando o template Djàvue...

No começo deste ano contribuí bastante para a versão 3 deste template, e achei que poderia utilizá-lo para me ajudar nesta entrega!

Este projeto segue a organização do Djàvue que pode ser [acessada aqui](https://github.com/evolutio/djavue3). Mais informações pode ser vista nesta documentação criada por mim mesmo aqui: [https://djavue.org/](https://www.djavue.org/README_EN.html)


## Fundação

- Gerenciador de pacotes (Poetry)
- dotenv para facilitar rodar em diferentes ambientes, escolher com ou sem Docker etc...
- API com documentação automática (swagger)
- Linter e formatador de código (Flake8 e Black)
- Pytest
- Docker para rodar tudo com 1 comando
- CI com GitHub Actions
- CD para deploy no Fly.io

### 🎥 ** VÍDEO 3:** Visão geral da solução
- 👉 [https://www.loom.com/share/0bd3730b1a894d8588c0620ac1632469](https://www.loom.com/share/0bd3730b1a894d8588c0620ac1632469)


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
        -auto_winner
    }
    class Competitor{
        -name
    }
```

## Iniciando - Rodando o projeto

## Requisitos

- Git
- 🐍 Python 3.11.x
- Um terminal (de preferência um terminal Linux, é para funcionar em um terminal WSL no Windows)

Temos três formas para **Rodar** 🍨:
- Sem Docker 📦: Apenas **Python** (usando sqlite)
- Apenas Banco de dados usando 🐋 Docker (melhor para debug)
- Tudo usando Docker 🐋: **Docker** and **Docker compose**


## Rodar local (min.dependências) SEM Docker 🦄

🌈 TIPS/TRICKS: Melhor utilizar Python 3.11 ou mais novo. Uma boa forma de gerenciar versões de python é utilizar ferramentas como [Pyenv](https://github.com/pyenv/pyenv) ou [asdf](https://github.com/asdf-vm/asdf) 

Clonar e entrar na pasta do projeto

```shell
git clone https://github.com/huogerac/wimbledon.git
cd wimbledon/
```

Vamos agora criar um ambiente virtual Python e instalar as dependências:

**AVISO**: Confirme que tem a versão correta do Python para este projeto

```shell
poetry config virtualenvs.in-project true    # cria o virtualenv na pasta .env
poetry install
```

- **IMPORTANTE**:
Vamos precisar confirmar como as variáveis de ambiente estão configuradas no arquivo `.env`, ou seja, precisamos garantir que a sessão 'Para uso local via virtualenv' estão sem comentário:

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

Agora, vamos criar as migrações, ou seja, as tabelas iniciais do projeto (com base nas definições dos models). Note que o Django já vem com alguns problemas resolvidos, então vamos ter umas tabelas a mais, como usuário e sessões. Pode parecer estranho para este projeto, mas no mundo real, não queremos qualquer pessoa enviando resultado dos jogos, logo vamos precisar de autenticação. 

**Nota:** Neste momento, todos endpoints estão abertos, mas é bem fácil protegê-los

**IMPORTANTE:**
- Como estamos utilizando Poetry, vamos precisar rodar os comandos com `poetry run [comando]` ou abrir o shell com `poetry shell` antes de digitar os comandos a seguir:

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

torneio = Tournament.objects.create(description='Wimbledon 2024')
torneio.save()

competidores = 'Alex|Diana|Polina|Kristina|Mara Guth|John Doe|Oliva||Rafael'.split('|')
[tournaments_svc.create_competitor(torneio.id, name) for name in players]

tournaments_svc.start_tournament(torneio.id)
tournaments_svc.list_matches(torneio.id)

```


## Rodar tudo com 🐋 (Usando Postgres)

**Requirements:**

- Docker version >= 24.0.2 (in any S.O. you have)
- Docker Compose version >= v2.18.1
- Um terminal Linux ou WSL no Windows

Como a aplicação se comporta em tempo de execução é com base nas configurações do settings para um determinado ambiente seguindo o [12 factors](https://12factor.net/), desta forma, podemos conectar em um sqllite ou em Postgres, pode ser em modo DEBUG ou não. Estas configurações estão no arquivo .env

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

Primeiramente, independente de qual diretório você está, veja se já existe algum container iniciado. De preferência, tente parar ou apagar os containers e deixar a listagem vazia.

```shell
docker ps

CONTAINER ID   IMAGE  COMMAND      CREATED       STATUS                PORTS 
``` 

👉 **INFO**:
Se sua lista exibir algum container, você precisa fazer um `docker stop [CONTAINER ID]`


Entre no diretório do projeto

```shell
cd wimbledon/
```

Digite o comando para iniciar os containers em modo "detached"

```shell
docker compose up -d
```

Depois de baixar as camadas e fazer o "build" das imagens, digite novamente o comando `docker ps`, ele deverá listar dois containers: o backend e o banco de dados Postgres rodando:

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
    image: "postgres:14-alpine"
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

Você pode acessar o container **backend container** e digitar os mesmos comandos utilizados sem docker, primeiro é necessário entrar dentro do container:

```shell
docker compose exec -it backend bash
```

Uma vez dentro do container, podemos digitar os comandos do Django como mostrado na seção anterior (Rodar sem docker)

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
    Models *-- Manager
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

# Entendendo o negócio

Comece pelos testes! Neles devemos entender as regras existentes.
Os testes estão divididos inicialmente em duas camadas:
- Testes da **camada da API**: Onde é validado se um endpoint retorna 200 ou 201, se da erro 400 quando tem input inválido, ou seja, regras relacionadas ao contrato da API
- Testes da **camada de SERVIÇO**: Onde é validado as regras de negócio, por exemplo, se podemos ter dois competidores com o mesmo nome dentro do mesmo torneio. Ou se podemos enviar resultado de uma partida para uma partida que já possui resultado.

```shell
core/tests/
    ├── conftest.py
    ├── test_api_01_novos_torneios.py           👉 Teste da API
    ├── test_api_02_listar_torneios.py
    ├── test_svc_01_novos_torneios.py           👉 Teste dos serviços
    ├── test_svc_02_cadastro_competidores.py
    ├── test_svc_03_iniciar_partidas.py
    ├── test_svc_04_listar_partidas.py
    ├── test_svc_05_cadastrar_resultados.py
    └── test_svc_06_listar_top4.py

```

## TODO

- [x] salvar resultado
- [x] salvar resultado revisando prox. game/level
- [x] mvp frontend para visualizar resultados
- [x] escrever mais testes
- [x] listar top 4
- [x] remover accounts
- [x] doc inicial
- [x] Poetry
- [x] Testar com docker e postgres
- [x] Deploy Fly.io
- [ ] Teste final com 17 jogadores
- [ ] Tipar os tipos parâmetros, ex. tournament_id esta string
- [ ] Melhorar listar matches
- [ ] Caso de marcar torneio como completo
- [ ] Listar tournament
- [ ] Bug 6 jogadores que na fase dois temos numero ímpar de competidores
- [ ] Nao permitir incluir novos competidores qdo tem matches (inicializado)
- [ ] Adicionar o output da solucao 1


## Testes

```python

from wimbledon.core.service import tournaments_svc

tour = Tournament.objects.all().first()

OU

Tournament.objects.get(id=2)
<Tournament: Wimbledon 2024>
tour = _

# Cadastra competidores
players = 'Alex Eala|Diana Shnaider|Polina Kudermetova|Kristina Dmitruk|Germany Mara Guth|John Doe|Oliva Galvones|Player One|Player Two|Rafael Nadal|Roger Federer|Leo Borg|Bruno Kuzuhara|Daniel Aguilar|Ethan Quinn|Tarantino'.split('|')

[tournaments_svc.create_competitor(tour.id, name) for name in players]

[{'id': 2, 'tournament_id': 2, 'name': 'Alex Eala'},
 {'id': 3, 'tournament_id': 2, 'name': 'Diana Shnaider'},
 {'id': 4, 'tournament_id': 2, 'name': 'Polina Kudermetova'},
 {'id': 5, 'tournament_id': 2, 'name': 'Kristina Dmitruk'},
 {'id': 6, 'tournament_id': 2, 'name': 'Germany Mara Guth'},
 {'id': 7, 'tournament_id': 2, 'name': 'John Doe'},
 {'id': 8, 'tournament_id': 2, 'name': 'Oliva Galvones'},
 {'id': 9, 'tournament_id': 2, 'name': 'Player One'},
 {'id': 10, 'tournament_id': 2, 'name': 'Player Two'},
 {'id': 11, 'tournament_id': 2, 'name': 'Rafael Nadal'},
 {'id': 12, 'tournament_id': 2, 'name': 'Roger Federer'},
 {'id': 13, 'tournament_id': 2, 'name': 'Leo Borg'},
 {'id': 14, 'tournament_id': 2, 'name': 'Bruno Kuzuhara'},
 {'id': 15, 'tournament_id': 2, 'name': 'Daniel Aguilar'},
 {'id': 16, 'tournament_id': 2, 'name': 'Ethan Quinn'},
 {'id': 17, 'tournament_id': 2, 'name': 'Tarantino'}]

```


```python

import requests

# Listar torneios
requests.get(
  "http://localhost:8000/api/core/tournaments/",
  
).json()

# Cadastrar competidor
requests.post(
  "http://localhost:8000/api/core/tournaments/2/competitor",
  json={"name":"Rod Laver"},
).json()

# Listar competidores
requests.get(
  "http://localhost:8000/api/core/tournaments/2/competitor",
).json()

# Listar partidas
requests.get(
  "http://localhost:8000/api/core/tournaments/2/match",
).json()

# Listar top 4
requests.get(
  "http://localhost:8000/api/core/tournaments/2/result",
).json()

```

## ❌ Limitações/Problemas conhecidos

- Depende o número de competidores, o gerador de matches vai falhar. Embora ele funcione para número ímpar de competidores, alguns números como 17 competidores, irá gerar um jogador que ficará sem jogar.
- Alguns endpoints da API estão com tratamento de erros, mas vários estão sem
- Podemos melhorar a tipagem dos dados na camada da API e de serviço, por exemplo, dizer que id é int
- Melhorar a padronização, na api temos tournaments no plural e match no singular
- Escrever mais testes para cobrir mais casos alternativos
- Falta mais tratamento de 404
- O método que calcula o 'level' do jogo falha dependendo do número de participantes. E está usando uma lógica ruim
