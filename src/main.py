"""TaskTracker: gerenciador de tarefas (Fase 2).

Uso:
    python3 src/main.py          # interface de linha de comando (padrão)
    python3 src/main.py --gui    # janela simples com botões (opcional)
"""

import sys

PRIORIDADES_VALIDAS = {
    "alta": "Alta",
    "média": "Média",
    "media": "Média",
    "baixa": "Baixa",
}

MENSAGEM_TITULO_VAZIO = "O título é obrigatório e não pode ficar vazio."
MENSAGEM_PRIORIDADE_INVALIDA = "Prioridade inválida. Use Alta, Média ou Baixa."
MENSAGEM_SEM_TAREFAS = "Nenhuma tarefa pendente no momento."
MENSAGEM_SUCESSO = "Tarefa cadastrada com sucesso!"


# ---------------------------------------------------------------------------
# Regras de negócio (compartilhadas pelo terminal e pela janela)
# ---------------------------------------------------------------------------

def titulo_valido(titulo):
    """O título não pode ser vazio nem composto apenas por espaços."""
    return bool(titulo.strip())


def normalizar_prioridade(texto):
    """Devolve 'Alta', 'Média' ou 'Baixa'; devolve None se a entrada for inválida."""
    return PRIORIDADES_VALIDAS.get(texto.strip().lower())


def criar_tarefa(titulo, descricao, prioridade, data_limite):
    """Monta o dicionário da tarefa; o status inicial é sempre 'Pendente'."""
    return {
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": "Pendente",
    }


def formatar_tarefa(numero, tarefa):
    """Texto legível com todas as propriedades de uma tarefa."""
    return (
        f"Tarefa {numero}\n"
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
    print("2. Visualizar tarefas cadastradas")
    print("3. Sair da aplicação")


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


def cadastrar_tarefa(tarefas):
    titulo = ler_titulo()
    descricao = input("Descrição: ").strip()
    prioridade = ler_prioridade()
    data_limite = input("Data limite (DD/MM/AAAA): ").strip()

    tarefas.append(criar_tarefa(titulo, descricao, prioridade, data_limite))
    print(f"\n{MENSAGEM_SUCESSO}")


def listar_tarefas(tarefas):
    if not tarefas:
        print(f"\n{MENSAGEM_SEM_TAREFAS}")
        return

    print("\n===== TAREFAS CADASTRADAS =====")
    for numero, tarefa in enumerate(tarefas, start=1):
        print(f"\n{formatar_tarefa(numero, tarefa)}")


def main():
    tarefas = []

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            print("\nEncerrando o TaskTracker. Até logo!")
            break
        else:
            print("\nOpção inválida. Digite 1, 2 ou 3.")


# ---------------------------------------------------------------------------
# Interface gráfica simples (opcional: python3 src/main.py --gui)
# ---------------------------------------------------------------------------

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
    campo_titulo = ttk.Entry(quadro, width=45)
    campo_titulo.grid(row=0, column=1, columnspan=3, pady=3)

    ttk.Label(quadro, text="Descrição:").grid(row=1, column=0, sticky="w", pady=3)
    campo_descricao = ttk.Entry(quadro, width=45)
    campo_descricao.grid(row=1, column=1, columnspan=3, pady=3)

    ttk.Label(quadro, text="Prioridade:").grid(row=2, column=0, sticky="w", pady=3)
    campo_prioridade = ttk.Combobox(
        quadro, values=["Alta", "Média", "Baixa"], width=42
    )
    campo_prioridade.grid(row=2, column=1, columnspan=3, pady=3)

    ttk.Label(quadro, text="Data limite:").grid(row=3, column=0, sticky="w", pady=3)
    campo_data = ttk.Entry(quadro, width=45)
    campo_data.grid(row=3, column=1, columnspan=3, pady=3)

    area_lista = tk.Text(quadro, width=58, height=12, state="disabled")
    area_lista.grid(row=5, column=0, columnspan=4, pady=(10, 0))

    def atualizar_lista():
        if tarefas:
            texto = "\n\n".join(
                formatar_tarefa(numero, tarefa)
                for numero, tarefa in enumerate(tarefas, start=1)
            )
        else:
            texto = MENSAGEM_SEM_TAREFAS
        area_lista.configure(state="normal")
        area_lista.delete("1.0", tk.END)
        area_lista.insert(tk.END, texto)
        area_lista.configure(state="disabled")

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
                titulo.strip(),
                campo_descricao.get().strip(),
                prioridade,
                campo_data.get().strip(),
            )
        )
        for campo in (campo_titulo, campo_descricao, campo_data):
            campo.delete(0, tk.END)
        campo_prioridade.set("")
        atualizar_lista()
        messagebox.showinfo("Sucesso", MENSAGEM_SUCESSO)

    ttk.Button(quadro, text="Cadastrar tarefa", command=cadastrar).grid(
        row=4, column=1, pady=10
    )
    ttk.Button(quadro, text="Visualizar tarefas", command=atualizar_lista).grid(
        row=4, column=2, pady=10
    )
    ttk.Button(quadro, text="Sair", command=janela.destroy).grid(
        row=4, column=3, pady=10
    )

    atualizar_lista()
    janela.mainloop()


if __name__ == "__main__":
    if "--gui" in sys.argv[1:]:
        iniciar_interface_grafica()
    else:
        main()
