"""TaskTracker: gerenciador de tarefas em linha de comando (Fase 2).

Uso:
    python3 src/main.py
"""

STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"

PRIORIDADES_VALIDAS = {
    "alta": "Alta",
    "média": "Média",
    "media": "Média",
    "baixa": "Baixa",
}

MENSAGEM_TITULO_VAZIO = "O título é obrigatório e não pode ficar vazio."
MENSAGEM_PRIORIDADE_INVALIDA = "Prioridade inválida. Use Alta, Média ou Baixa."
MENSAGEM_SUCESSO = "Tarefa cadastrada com sucesso!"
MENSAGEM_NAO_ENCONTRADA = "Não existe tarefa com o número {}."
MENSAGEM_LISTA_VAZIA = {
    STATUS_PENDENTE: "Nenhuma tarefa pendente no momento.",
    STATUS_CONCLUIDA: "Nenhuma tarefa concluída no momento.",
}
TITULO_LISTA = {
    STATUS_PENDENTE: "TAREFAS PENDENTES",
    STATUS_CONCLUIDA: "TAREFAS CONCLUÍDAS",
}


# ---------------------------------------------------------------------------
# Regras de negócio
# ---------------------------------------------------------------------------

def titulo_valido(titulo):
    """O título não pode ser vazio nem composto apenas por espaços."""
    return bool(titulo.strip())


def normalizar_prioridade(texto):
    """Devolve 'Alta', 'Média' ou 'Baixa'; devolve None se a entrada for inválida."""
    return PRIORIDADES_VALIDAS.get(texto.strip().lower())


def proximo_id(tarefas):
    """Número da próxima tarefa (cada tarefa mantém o seu número até ser excluída)."""
    return max((tarefa["id"] for tarefa in tarefas), default=0) + 1


def criar_tarefa(id_tarefa, titulo, descricao, prioridade, data_limite):
    """Monta o dicionário da tarefa; o status inicial é sempre 'Pendente'."""
    return {
        "id": id_tarefa,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": STATUS_PENDENTE,
    }


def filtrar_por_status(tarefas, status):
    return [tarefa for tarefa in tarefas if tarefa["status"] == status]


def buscar_tarefa(tarefas, id_tarefa):
    """Devolve a tarefa com o número informado ou None se ela não existir."""
    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            return tarefa
    return None


def concluir_tarefa(tarefas, id_tarefa):
    """Marca uma tarefa existente como concluída. Devolve (sucesso, mensagem)."""
    tarefa = buscar_tarefa(tarefas, id_tarefa)
    if tarefa is None:
        return False, MENSAGEM_NAO_ENCONTRADA.format(id_tarefa)
    if tarefa["status"] == STATUS_CONCLUIDA:
        return False, "Essa tarefa já está concluída."
    tarefa["status"] = STATUS_CONCLUIDA
    return True, "Tarefa concluída com sucesso!"


def excluir_tarefa(tarefas, id_tarefa):
    """Remove uma tarefa existente da lista. Devolve (sucesso, mensagem)."""
    tarefa = buscar_tarefa(tarefas, id_tarefa)
    if tarefa is None:
        return False, MENSAGEM_NAO_ENCONTRADA.format(id_tarefa)
    tarefas.remove(tarefa)
    return True, "Tarefa excluída com sucesso!"


def formatar_tarefa(tarefa):
    """Texto legível com todas as propriedades de uma tarefa."""
    return (
        f"Tarefa {tarefa['id']}\n"
        f"  Título:      {tarefa['titulo']}\n"
        f"  Descrição:   {tarefa['descricao']}\n"
        f"  Prioridade:  {tarefa['prioridade']}\n"
        f"  Data limite: {tarefa['data_limite']}\n"
        f"  Status:      {tarefa['status']}"
    )


# ---------------------------------------------------------------------------
# Interface de linha de comando
# ---------------------------------------------------------------------------

def exibir_menu():
    print("\n===== TASKTRACKER =====")
    print("1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas pendentes")
    print("3. Visualizar tarefas concluídas")
    print("4. Concluir tarefa")
    print("5. Excluir tarefa")
    print("6. Sair da aplicação")


def ler_titulo():
    """Repete o prompt até receber um título que não seja vazio nem só espaços."""
    while True:
        titulo = input("Título: ")
        if titulo_valido(titulo):
            return titulo.strip()
        print(f"Erro: {MENSAGEM_TITULO_VAZIO}")


def ler_prioridade():
    """Repete o prompt até receber Alta, Média (ou Media) ou Baixa."""
    while True:
        prioridade = normalizar_prioridade(input("Prioridade (Alta/Média/Baixa): "))
        if prioridade is not None:
            return prioridade
        print(f"Erro: {MENSAGEM_PRIORIDADE_INVALIDA}")


def ler_numero_tarefa(acao):
    """Pede o número de uma tarefa. Devolve None se o usuário cancelar (Enter)."""
    while True:
        entrada = input(f"Número da tarefa a {acao} (Enter para cancelar): ").strip()
        if not entrada:
            return None
        if entrada.isdecimal():
            return int(entrada)
        print("Erro: digite apenas o número da tarefa.")


def cadastrar_tarefa(tarefas):
    titulo = ler_titulo()
    descricao = input("Descrição: ").strip()
    prioridade = ler_prioridade()
    data_limite = input("Data limite (DD/MM/AAAA): ").strip()

    tarefas.append(
        criar_tarefa(proximo_id(tarefas), titulo, descricao, prioridade, data_limite)
    )
    print(f"\n{MENSAGEM_SUCESSO}")


def listar_tarefas(tarefas, status):
    selecionadas = filtrar_por_status(tarefas, status)
    if not selecionadas:
        print(f"\n{MENSAGEM_LISTA_VAZIA[status]}")
        return

    print(f"\n===== {TITULO_LISTA[status]} =====")
    for tarefa in selecionadas:
        print(f"\n{formatar_tarefa(tarefa)}")


def opcao_concluir_tarefa(tarefas):
    if not filtrar_por_status(tarefas, STATUS_PENDENTE):
        print(f"\n{MENSAGEM_LISTA_VAZIA[STATUS_PENDENTE]}")
        return

    listar_tarefas(tarefas, STATUS_PENDENTE)
    print()
    id_tarefa = ler_numero_tarefa("concluir")
    if id_tarefa is None:
        print("\nOperação cancelada.")
        return

    sucesso, mensagem = concluir_tarefa(tarefas, id_tarefa)
    print(f"\n{'' if sucesso else 'Erro: '}{mensagem}")


def opcao_excluir_tarefa(tarefas):
    if not tarefas:
        print("\nNenhuma tarefa cadastrada para excluir.")
        return

    for status in (STATUS_PENDENTE, STATUS_CONCLUIDA):
        if filtrar_por_status(tarefas, status):
            listar_tarefas(tarefas, status)
    print()
    id_tarefa = ler_numero_tarefa("excluir")
    if id_tarefa is None:
        print("\nOperação cancelada.")
        return

    tarefa = buscar_tarefa(tarefas, id_tarefa)
    if tarefa is None:
        print(f"\nErro: {MENSAGEM_NAO_ENCONTRADA.format(id_tarefa)}")
        return

    resposta = input(f'Confirma a exclusão da tarefa "{tarefa["titulo"]}"? (s/n): ')
    if resposta.strip().lower() in ("s", "sim"):
        _, mensagem = excluir_tarefa(tarefas, id_tarefa)
        print(f"\n{mensagem}")
    else:
        print("\nExclusão cancelada.")


def main():
    tarefas = []

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas, STATUS_PENDENTE)
        elif opcao == "3":
            listar_tarefas(tarefas, STATUS_CONCLUIDA)
        elif opcao == "4":
            opcao_concluir_tarefa(tarefas)
        elif opcao == "5":
            opcao_excluir_tarefa(tarefas)
        elif opcao == "6":
            print("\nEncerrando o TaskTracker. Até logo!")
            break
        else:
            print("\nOpção inválida. Digite um número de 1 a 6.")


if __name__ == "__main__":
    main()
