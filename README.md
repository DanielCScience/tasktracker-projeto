# TaskTracker

Aplicação de linha de comando (CLI) em Python 3 para cadastrar e acompanhar tarefas.
Projeto do **Bootcamp II — Engenharia de Software, Versionamento Profissional de Código e
Desenvolvimento de Sistemas** (Fase 2 — Entrega Intermediária).

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

> Nesta fase as tarefas ficam apenas em memória, enquanto o programa está aberto.

## Tecnologias

- Python 3.8 ou superior (somente biblioteca padrão, sem dependências externas)
- Git e GitHub para versionamento

## Estrutura do repositório

```text
tasktracker-projeto/
├── README.md                     # Documentação principal e instruções de uso
├── .gitignore                    # Ignora arquivos temporários do Python e ambiente virtual
├── docs/
│   └── planejamento_logico.pdf   # Planejamento lógico e arquitetural (Fase 1)
└── src/
    └── main.py                   # Código-fonte da aplicação
```

## Instalação e execução

```bash
# 1. Clonar o repositório
git clone https://github.com/<seu-usuario>/tasktracker-projeto.git
cd tasktracker-projeto

# 2. Executar (não há dependências para instalar)
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
Título: Estudar Git
Descrição: Revisar commit, branch e push
Prioridade (Alta/Média/Baixa): urgente
Erro: Prioridade inválida. Use Alta, Média ou Baixa.
Prioridade (Alta/Média/Baixa): Alta
Data limite (DD/MM/AAAA): 20/10/2026

Tarefa cadastrada com sucesso!
```

Concluindo a tarefa criada acima (opção 4):

```text
===== TAREFAS PENDENTES =====

Tarefa 1
  Título:      Estudar Git
  Descrição:   Revisar commit, branch e push
  Prioridade:  Alta
  Data limite: 20/10/2026
  Status:      Pendente

Número da tarefa a concluir (Enter para cancelar): 1

Tarefa concluída com sucesso!
```

## Autor

**Daniel Lourenço Lustosa** — Ciências da Computação, CEUB.

## Roadmap

- **Fase 1**: planejamento lógico e arquitetura de dados (concluída)
- **Fase 2**: repositório Git/GitHub e implementação em Python (esta entrega)
- **Fase 3**: empacotamento, containerização com Docker, testes e deploy
