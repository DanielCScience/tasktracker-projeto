# TaskTracker

Aplicação de linha de comando (CLI) em Python 3 para cadastrar e acompanhar tarefas.
Projeto do **Bootcamp II — Engenharia de Software, Versionamento Profissional de Código e
Desenvolvimento de Sistemas** (Fase 2 — Entrega Intermediária).

## Descrição funcional

O TaskTracker oferece um menu contínuo no terminal com três opções:

1. **Cadastrar nova tarefa**: solicita título, descrição, prioridade e data limite.
2. **Visualizar tarefas cadastradas**: lista todas as tarefas com seus campos.
3. **Sair da aplicação**.

### Campos e regras de negócio

| Campo       | Regra                                                                                     |
|-------------|-------------------------------------------------------------------------------------------|
| Título      | Obrigatório. Entradas vazias ou só com espaços são rejeitadas e o prompt é repetido.      |
| Descrição   | Texto livre.                                                                              |
| Prioridade  | Aceita somente `Alta`, `Média` (ou `Media`) e `Baixa`, sem diferenciar maiúsculas/minúsculas. Outras entradas geram erro e repetem o prompt. |
| Data limite | Texto livre ou `DD/MM/AAAA`.                                                              |
| Status      | Definido automaticamente como `Pendente` no cadastro.                                     |

Se nenhuma tarefa foi cadastrada, a listagem exibe a mensagem "Nenhuma tarefa pendente no momento.",
conforme definido no algoritmo do planejamento lógico (`docs/planejamento_logico.pdf`).

> Nesta fase as tarefas ficam apenas em memória, enquanto o programa está aberto.

## Tecnologias

- Python 3.8 ou superior (somente biblioteca padrão, sem dependências externas;
  `tkinter` apenas para a interface gráfica opcional)
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

### Interface gráfica (opcional)

Além do menu no terminal, há uma janela simples com botões (**Cadastrar tarefa**,
**Visualizar tarefas** e **Sair**), que usa as mesmas regras de validação:

```bash
python3 src/main.py --gui
```

Ela usa o `tkinter`, que já acompanha o Python no Windows e no macOS. No Linux
(Debian/Ubuntu), instale com `sudo apt install python3-tk`. Sem `--gui`, o programa
abre normalmente a interface de linha de comando.

## Exemplo de uso

```text
===== TASKTRACKER =====
1. Cadastrar nova tarefa
2. Visualizar tarefas cadastradas
3. Sair da aplicação
Escolha uma opção: 1

Título: 
Erro: o título é obrigatório e não pode ficar vazio.
Título: Estudar Git
Descrição: Revisar commit, branch e push
Prioridade (Alta/Média/Baixa): urgente
Erro: prioridade inválida. Use Alta, Média ou Baixa.
Prioridade (Alta/Média/Baixa): Alta
Data limite (DD/MM/AAAA): 20/10/2026

Tarefa cadastrada com sucesso!
```

## Autor

**Daniel Lourenço Lustosa** — Ciências da Computação, CEUB.

## Roadmap

- **Fase 1**: planejamento lógico e arquitetura de dados (concluída)
- **Fase 2**: repositório Git/GitHub e implementação em Python (esta entrega)
- **Fase 3**: empacotamento, containerização com Docker, testes e deploy
