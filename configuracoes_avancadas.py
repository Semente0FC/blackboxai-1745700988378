import tkinter as tk
import ctypes

# Variáveis de configuração padrão
config = {
    "break_even": True,
    "pips_be": 15,
    "offset_be": 2,
    "trailing": True,
    "pips_trailing_start": 25,
    "pips_trailing_distancia": 10,
    "meta_diaria": 3,
    "parar_ao_bater_meta": True
}

def abrir_configuracoes(janela_pai):
    # 🟰 Pega o tema do painel
    bg_color = janela_pai.cget("bg")
    if bg_color in ("#121212", "#1E1E1E", "#000000"):  # Se for escuro
        tema_escuro = True
    else:
        tema_escuro = False

    # Define cores baseadas no tema atual
    if tema_escuro:
        bg_color = "#121212"
        fg_color = "white"
        card_color = "#1E1E1E"
    else:
        bg_color = "#F0F0F0"
        fg_color = "black"
        card_color = "#FFFFFF"

    config_window = tk.Toplevel(janela_pai)
    config_window.title("Configurações Avançadas")
    config_window.geometry("400x500")
    center_window(config_window, 400, 500)
    config_window.resizable(False, False)
    aplicar_borda_arredondada(config_window)

    config_window.configure(bg=bg_color)

    title = tk.Label(config_window, text="⚙️ Configurações Avançadas", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color)
    title.pack(pady=10)

    frame = tk.Frame(config_window, bg=card_color, bd=2, relief="groove")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    labels = [
        ("Break Even", "break_even"),
        ("Pips para ativar BE", "pips_be"),
        ("Offset do BE", "offset_be"),
        ("Trailing Stop", "trailing"),
        ("Pips para iniciar trailing", "pips_trailing_start"),
        ("Distância trailing (pips)", "pips_trailing_distancia"),
        ("Meta diária de lucro (%)", "meta_diaria"),
        ("Parar ao bater meta", "parar_ao_bater_meta")
    ]

    entradas = {}

    for idx, (texto, chave) in enumerate(labels):
        label = tk.Label(frame, text=texto, bg=card_color, fg=fg_color, anchor="w", font=("Arial", 11))
        label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

        if isinstance(config[chave], bool):
            var = tk.IntVar(value=int(config[chave]))
            chk = tk.Checkbutton(frame, variable=var, bg=card_color, fg=fg_color, selectcolor=card_color, activebackground=card_color)
            chk.grid(row=idx, column=1, sticky="e", padx=10)
            entradas[chave] = var
        else:
            entrada = tk.Entry(frame, width=10)
            entrada.insert(0, str(config[chave]))
            entrada.grid(row=idx, column=1, padx=10, pady=5)
            entradas[chave] = entrada

    def salvar():
        for chave, widget in entradas.items():
            if isinstance(widget, tk.Entry):
                valor = float(widget.get())
            else:
                valor = bool(widget.get())
            config[chave] = valor
        config_window.destroy()

    botao_salvar = tk.Button(config_window, text="💾 Salvar Configurações", command=salvar, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=25)
    botao_salvar.pack(pady=20)

def aplicar_borda_arredondada(janela):
    try:
        hwnd = ctypes.windll.user32.GetParent(janela.winfo_id())
        class MARGINS(ctypes.Structure):
            _fields_ = [("cxLeftWidth", ctypes.c_int),
                        ("cxRightWidth", ctypes.c_int),
                        ("cyTopHeight", ctypes.c_int),
                        ("cyBottomHeight", ctypes.c_int)]
        margins = MARGINS(2, 2, 2, 2)
        ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
    except:
        pass

def center_window(janela, width, height):
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (width // 2)
    y = (janela.winfo_screenheight() // 2) - (height // 2)
    janela.geometry(f"{width}x{height}+{x}+{y}")
