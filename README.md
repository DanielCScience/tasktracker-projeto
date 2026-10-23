# TaskTracker

Aplicação de linha de comando (CLI) em Python 3 para cadastrar e acompanhar tarefas,
empacotada em um container **Docker** e orquestrada com **Docker Compose**.
Projeto do **Bootcamp II — Engenharia de Software, Versionamento Profissional de Código e
Desenvolvimento de Sistemas** (Fase 3 — Entrega Final: Conteinerização, Orquestração e Deploy).

## Descrição funcional

O TaskTracker oferece um menu contínuo no terminal:

1. **Cadastrar nova tarefa**: solicita título, descrição, prioridade e data limite.
2. **Visualizar tarefas pendentes**: lista apenas as tarefas ainda não concluídas.
3. **Visualizar tarefas concluídas**: lista apenas as tarefas já concluídas.
4. **Concluir tarefa**: marca uma tarefa pendente como concluída.
5. **Excluir tarefa**: remove uma tarefa (pendente ou concluída), com confirmação.
6. **Sair da aplicação**.

### Campos e regras de negócio

| Campo       | Regra                                                                                     |
|-------------|-------------------------------------------------------------------------------------------|
| Nº          | Gerado automaticamente. Identifica a tarefa ao concluir ou excluir.                       |
| Título      | Obrigatório. Entradas vazias ou só com espaços são rejeitadas e o prompt é repetido.      |
| Descrição   | Texto livre.                                                                              |
| Prioridade  | Aceita somente `Alta`, `Média` (ou `Media`) e `Baixa`, sem diferenciar maiúsculas/minúsculas. Outras entradas geram erro e repetem o prompt. |
| Data limite | Texto livre ou `DD/MM/AAAA`.                                                              |
| Status      | `Pendente` no cadastro; passa a `Concluída` quando a tarefa é concluída.                  |

Regras adicionais:

- Não é possível concluir nem excluir uma tarefa que não existe: o sistema exibe uma
  mensagem de erro e volta ao menu.
- Uma tarefa já concluída não pode ser concluída novamente.
- Se não houver tarefas pendentes, a listagem exibe "Nenhuma tarefa pendente no momento.",
  conforme definido no algoritmo do planejamento lógico (`docs/planejamento_logico.pdf`).
  Para as concluídas, a mensagem é "Nenhuma tarefa concluída no momento."

> As tarefas ficam apenas em memória, enquanto o programa está aberto. Ao sair da aplicação,
> o container é encerrado e a lista é descartada.

## Tecnologias

- Python 3.11 (somente biblioteca padrão, sem dependências externas)
- Docker e Docker Compose
- Git e GitHub para versionamento

## Estrutura do repositório

```text
tasktracker-projeto/
├── .gitignore                    # Ignora arquivos temporários do Python e ambiente virtual
├── docs/
│   └── planejamento_logico.pdf   # Planejamento lógico e arquitetural (Fase 1)
├── src/
│   └── main.py                   # Código-fonte da aplicação (Fase 2)
├── Dockerfile                    # Receita da imagem Docker (Fase 3)
├── docker-compose.yml            # Orquestração da execução interativa (Fase 3)
└── README.md                     # Documentação principal e guia Docker
```

## Guia Docker

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado e em execução (no Windows e no
  macOS, o Docker Desktop precisa estar aberto). O Docker Compose já vem junto com o Docker.
- Git, para clonar o repositório.

### Baixar o projeto

```bash
git clone https://github.com/DanielCScience/tasktracker-projeto.git
cd tasktracker-projeto
```

Execute os comandos abaixo **dentro da pasta `tasktracker-projeto`**, onde ficam o
`Dockerfile` e o `docker-compose.yml`.

### Como construir a imagem

```bash
docker build -t tasktracker-app .
```

### Como rodar o container em modo isolado

```bash
docker run -it --rm tasktracker-app
```

### Como rodar via orquestração (Recomendado)

```bash
docker compose run --rm tasktracker-app
```

O menu do TaskTracker aparece no terminal. Para encerrar, escolha a opção **6. Sair da
aplicação**.

### Por que `-it` e o `docker-compose.yml`?

A aplicação lê o teclado com `input()`, mas um container isolado não recebe digitação por
padrão. Por isso a execução precisa abrir um canal interativo:

| Onde                  | Opção                 | Função                                            |
|-----------------------|-----------------------|---------------------------------------------------|
| `docker run`          | `-i`                  | Mantém a entrada de dados (stdin) aberta.         |
| `docker run`          | `-t`                  | Aloca um terminal virtual (TTY).                  |
| `docker-compose.yml`  | `stdin_open: true`    | Equivale ao `-i`: mantém o stdin aberto.          |
| `docker-compose.yml`  | `tty: true`           | Equivale ao `-t`: aloca um terminal virtual.      |

A opção `--rm` apenas remove o container ao final da execução, sem deixar lixo no Docker.

### Como funciona o Dockerfile

| Instrução                         | O que faz                                                    |
|-----------------------------------|--------------------------------------------------------------|
| `FROM python:3.11-slim`           | Cria a base leve do sistema, com Python 3.11.                |
| `WORKDIR /app`                    | Define a pasta central de operações dentro do container.     |
| `ENV PYTHONUNBUFFERED=1`          | Garante a saída imediata (sem buffer) dos prompts e logs.    |
| `COPY src/ /app/src/`             | Injeta o código local no container.                          |
| `CMD ["python", "src/main.py"]`   | Dispara a execução da aplicação.                             |

### Dockerfile × docker-compose.yml

| Arquivo              | Papel                                          | Saída                          | Comando-chave        |
|----------------------|------------------------------------------------|--------------------------------|----------------------|
| `Dockerfile`         | Empacota a aplicação e suas dependências.      | Gera a imagem.                 | `docker build`       |
| `docker-compose.yml` | Orquestra a execução interativa da CLI.        | Roda o container com parâmetros. | `docker compose run` |

## Execução sem Docker (opcional)

Com o Python 3.8 ou superior instalado, não há dependências para instalar:

```bash
python3 src/main.py
```

No Windows, use `python src/main.py` caso `python3` não esteja disponível.

## Exemplo de uso

```text
===== TASKTRACKER =====
1. Cadastrar nova tarefa
2. Visualizar tarefas pendentes
3. Visualizar tarefas concluídas
4. Concluir tarefa
5. Excluir tarefa
6. Sair da aplicação
Escolha uma opção: 1

Título:
Erro: O título é obrigatório e não pode ficar vazio.
Título: Estudar Docker
Descrição: Construir a imagem e rodar o container
Prioridade (Alta/Média/Baixa): urgente
Erro: Prioridade inválida. Use Alta, Média ou Baixa.
Prioridade (Alta/Média/Baixa): Alta
Data limite (DD/MM/AAAA): 30/10/2026

Tarefa cadastrada com sucesso!
```

Concluindo a tarefa criada acima (opção 4):

```text
===== TAREFAS PENDENTES =====

Tarefa 1
  Título:      Estudar Docker
  Descrição:   Construir a imagem e rodar o container
  Prioridade:  Alta
  Data limite: 30/10/2026
  Status:      Pendente

Número da tarefa a concluir (Enter para cancelar): 1

Tarefa concluída com sucesso!
```

## Autor

**Daniel Lourenço Lustosa** — Ciências da Computação, CEUB.

## Roadmap

- **Fase 1**: planejamento lógico e arquitetura de dados (concluída)
- **Fase 2**: repositório Git/GitHub e implementação em Python (concluída)
- **Fase 3**: conteinerização com Docker, orquestração com Docker Compose e documentação (esta entrega)
