"""TaskTracker: gerenciador de tarefas (Fase 2).

Uso:
    python3 src/main.py          # interface de linha de comando (padrão)
    python3 src/main.py --gui    # janela simples com botões (opcional)
"""

import sys

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
# Regras de negócio (compartilhadas pelo terminal e pela janela)
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
# Interface de linha de comando (padrão)
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


# ---------------------------------------------------------------------------
# Interface gráfica simples (opcional: python3 src/main.py --gui)
# ---------------------------------------------------------------------------

COLUNAS_TABELA = (
    ("id", "Nº", 40),
    ("titulo", "Título", 150),
    ("descricao", "Descrição", 190),
    ("prioridade", "Prioridade", 80),
    ("data_limite", "Data limite", 90),
    ("status", "Status", 80),
)


def iniciar_interface_grafica():
    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
    except ImportError:
        print("O tkinter não está instalado neste Python.")
        print("No Linux (Debian/Ubuntu): sudo apt install python3-tk")
        print("Enquanto isso, use o modo terminal: python3 src/main.py")
        return

    tarefas = []

    janela = tk.Tk()
    janela.title("TaskTracker")
    janela.resizable(False, False)

    quadro = ttk.Frame(janela, padding=12)
    quadro.grid(row=0, column=0)

    ttk.Label(quadro, text="Título:").grid(row=0, column=0, sticky="w", pady=3)
    campo_titulo = ttk.Entry(quadro, width=60)
    campo_titulo.grid(row=0, column=1, columnspan=3, sticky="we", pady=3)

    ttk.Label(quadro, text="Descrição:").grid(row=1, column=0, sticky="w", pady=3)
    campo_descricao = ttk.Entry(quadro, width=60)
    campo_descricao.grid(row=1, column=1, columnspan=3, sticky="we", pady=3)

    ttk.Label(quadro, text="Prioridade:").grid(row=2, column=0, sticky="w", pady=3)
    campo_prioridade = ttk.Combobox(quadro, values=["Alta", "Média", "Baixa"], width=57)
    campo_prioridade.grid(row=2, column=1, columnspan=3, sticky="we", pady=3)

    ttk.Label(quadro, text="Data limite:").grid(row=3, column=0, sticky="w", pady=3)
    campo_data = ttk.Entry(quadro, width=60)
    campo_data.grid(row=3, column=1, columnspan=3, sticky="we", pady=3)

    def criar_tabela(linha, rotulo):
        ttk.Label(quadro, text=rotulo).grid(
            row=linha, column=0, columnspan=4, sticky="w", pady=(12, 2)
        )
        tabela = ttk.Treeview(
            quadro,
            columns=[chave for chave, _, _ in COLUNAS_TABELA],
            show="headings",
            height=5,
            selectmode="browse",
        )
        for chave, titulo, largura in COLUNAS_TABELA:
            tabela.heading(chave, text=titulo)
            tabela.column(chave, width=largura, anchor="w")
        tabela.grid(row=linha + 1, column=0, columnspan=4, sticky="we")
        aviso = ttk.Label(quadro, text="")
        aviso.grid(row=linha + 2, column=0, columnspan=4, sticky="w")
        return tabela, aviso

    tabela_pendentes, aviso_pendentes = criar_tabela(5, "Tarefas pendentes")
    tabela_concluidas, aviso_concluidas = criar_tabela(8, "Tarefas concluídas")

    def preencher(tabela, aviso, status):
        tabela.delete(*tabela.get_children())
        selecionadas = filtrar_por_status(tarefas, status)
        for tarefa in selecionadas:
            tabela.insert(
                "",
                tk.END,
                iid=str(tarefa["id"]),
                values=(
                    tarefa["id"],
                    tarefa["titulo"],
                    tarefa["descricao"],
                    tarefa["prioridade"],
                    tarefa["data_limite"],
                    tarefa["status"],
                ),
            )
        aviso.configure(text="" if selecionadas else MENSAGEM_LISTA_VAZIA[status])

    def atualizar_listas():
        preencher(tabela_pendentes, aviso_pendentes, STATUS_PENDENTE)
        preencher(tabela_concluidas, aviso_concluidas, STATUS_CONCLUIDA)

    def tarefa_selecionada(*tabelas):
        for tabela in tabelas:
            selecao = tabela.selection()
            if selecao:
                return int(selecao[0])
        return None

    def ao_selecionar(tabela, outra):
        """Mantém apenas uma linha selecionada entre as duas listas."""
        def tratar(_evento=None):
            if tabela.selection():
                outra_selecao = outra.selection()
                if outra_selecao:
                    outra.selection_remove(*outra_selecao)
        return tratar

    tabela_pendentes.bind(
        "<<TreeviewSelect>>", ao_selecionar(tabela_pendentes, tabela_concluidas)
    )
    tabela_concluidas.bind(
        "<<TreeviewSelect>>", ao_selecionar(tabela_concluidas, tabela_pendentes)
    )

    def cadastrar():
        titulo = campo_titulo.get()
        if not titulo_valido(titulo):
            messagebox.showerror("Erro", MENSAGEM_TITULO_VAZIO)
            campo_titulo.focus_set()
            return

        prioridade = normalizar_prioridade(campo_prioridade.get())
        if prioridade is None:
            messagebox.showerror("Erro", MENSAGEM_PRIORIDADE_INVALIDA)
            campo_prioridade.focus_set()
            return

        tarefas.append(
            criar_tarefa(
                proximo_id(tarefas),
                titulo.strip(),
                campo_descricao.get().strip(),
                prioridade,
                campo_data.get().strip(),
            )
        )
        for campo in (campo_titulo, campo_descricao, campo_data):
            campo.delete(0, tk.END)
        campo_prioridade.set("")
        atualizar_listas()
        messagebox.showinfo("Sucesso", MENSAGEM_SUCESSO)

    def concluir():
        id_tarefa = tarefa_selecionada(tabela_pendentes)
        if id_tarefa is None:
            messagebox.showerror(
                "Erro", "Selecione uma tarefa pendente na lista para concluir."
            )
            return
        sucesso, mensagem = concluir_tarefa(tarefas, id_tarefa)
        atualizar_listas()
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showerror("Erro", mensagem)

    def excluir():
        id_tarefa = tarefa_selecionada(tabela_pendentes, tabela_concluidas)
        if id_tarefa is None:
            messagebox.showerror("Erro", "Selecione uma tarefa em uma das listas para excluir.")
            return
        tarefa = buscar_tarefa(tarefas, id_tarefa)
        if tarefa is None:
            messagebox.showerror("Erro", MENSAGEM_NAO_ENCONTRADA.format(id_tarefa))
            atualizar_listas()
            return
        if not messagebox.askyesno(
            "Confirmar exclusão", f'Excluir a tarefa "{tarefa["titulo"]}"?'
        ):
            return
        _, mensagem = excluir_tarefa(tarefas, id_tarefa)
        atualizar_listas()
        messagebox.showinfo("Sucesso", mensagem)

    barra_botoes = ttk.Frame(quadro)
    barra_botoes.grid(row=4, column=0, columnspan=4, sticky="w", pady=10)
    ttk.Button(barra_botoes, text="Cadastrar tarefa", command=cadastrar).grid(
        row=0, column=0, padx=(0, 8)
    )
    ttk.Button(barra_botoes, text="Concluir selecionada", command=concluir).grid(
        row=0, column=1, padx=(0, 8)
    )
    ttk.Button(barra_botoes, text="Excluir selecionada", command=excluir).grid(
        row=0, column=2, padx=(0, 8)
    )
    ttk.Button(barra_botoes, text="Sair", command=janela.destroy).grid(
        row=0, column=3
    )

    atualizar_listas()
    janela.mainloop()


if __name__ == "__main__":
    if "--gui" in sys.argv[1:]:
        iniciar_interface_grafica()
    else:
        main()
