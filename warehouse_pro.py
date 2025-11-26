#antes de iniciar, instale esse modulo:#
pip install ttkbootstrap pandas pillow



import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import pandas as pd

# -----------------------------------------
# CONFIGURAÇÃO DO ARMAZÉM
# -----------------------------------------

layout_corredores = {
    "A": 5,
    "B": 6,
    "C": 6,
    "D": 7,
    "E": 6,
    "F": 6,
    "G": 6,
    "H": 6,
    "I": 6,
    "Corridor 5": 6
}

ALTURAS = 3

locais = {}
estoque = {}
rectangles = {}
cores = {}

# -----------------------------------------
# GERAR CORREDORES INTERNOS
# -----------------------------------------

def gerar_locais():
    for corredor, prateleiras in layout_corredores.items():
        for p in range(1, prateleiras + 1):
            for h in range(ALTURAS):
                nome = f"{corredor}-{p}-{h}"
                locais[nome] = {"tipo": "corredor"}

gerar_locais()

# -----------------------------------------
# FUNÇÕES DO SISTEMA
# -----------------------------------------

def importar_excel():
    caminho = entry_excel.get().strip()
    try:
        df = pd.read_excel(caminho)
    except:
        messagebox.showerror("Erro", "Não foi possível carregar o arquivo Excel.")
        return

    for _, row in df.iterrows():
        sku = str(row["SKU"])
        estoque[sku] = {
            "nome": row["Nome"],
            "quantidade": int(row["Quantidade"]),
            "local": row["Local"]
        }

    messagebox.showinfo("OK", "Dados importados com sucesso!")

def adicionar_local_extra():
    nome = entry_local.get().strip()

    if nome == "":
        messagebox.showerror("Erro", "Digite um nome.")
        return

    if nome in locais:
        messagebox.showerror("Erro", "Local já existe.")
        return

    locais[nome] = {"tipo": "extra"}

    desenhar_mapa()

    entry_local.delete(0, tk.END)
    messagebox.showinfo("OK", f"Local '{nome}' adicionado!")

def buscar_sku():
    sku = entry_sku.get().strip()

    if sku not in estoque:
        messagebox.showerror("Erro", "SKU não encontrado.")
        return

    local = estoque[sku]["local"]
    messagebox.showinfo("Localizado", f"O SKU está em: {local}")
    destacar(local)

def destacar(local):
    if local not in rectangles:
        return

    canvas.itemconfig(rectangles[local], fill="yellow")

    root.after(2000, lambda: canvas.itemconfig(rectangles[local], fill=cores[local]))

# -----------------------------------------
# DESENHO DO MAPA (VERSÃO AVANÇADA)
# -----------------------------------------

def desenhar_mapa():

    canvas.delete("all")
    rectangles.clear()
    cores.clear()

    offset_x = 50
    offset_y = 50

    for corredor, prateleiras in layout_corredores.items():

        canvas.create_text(offset_x, offset_y, text=f"Corredor {corredor}",
                           font=("Segoe UI", 14, "bold"), anchor="w")

        x = offset_x + 150
        y = offset_y

        for p in range(1, prateleiras + 1):

            for h in range(ALTURAS):

                nome = f"{corredor}-{p}-{h}"

                cor = "#91c2ff"
                cores[nome] = cor

                rect = canvas.create_rectangle(
                    x, y + h * 45,
                    x + 90, y + h * 45 + 40,
                    fill=cor, outline="#003d80", width=2
                )

                rectangles[nome] = rect

                canvas.create_text(x + 45, y + h * 45 + 20, text=f"{p}-{h}",
                                   font=("Segoe UI", 10, "bold"))

            x += 120

        offset_y += 180

    canvas.create_text(50, offset_y, text="Locais Extras", font=("Segoe UI", 14, "bold"))

    x = 200
    y = offset_y + 40

    for nome, info in locais.items():
        if info["tipo"] == "extra":

            cor = "#ffb5b5"
            cores[nome] = cor

            rect = canvas.create_rectangle(
                x, y,
                x + 150, y + 50,
                fill=cor, outline="#8b0000", width=2
            )

            rectangles[nome] = rect

            canvas.create_text(x + 75, y + 25, text=nome,
                               font=("Segoe UI", 11, "bold"))

            x += 180

# -----------------------------------------
# SUPORTE A ARRASTAR / ZOOM
# -----------------------------------------

def mouse_press(event):
    canvas.scan_mark(event.x, event.y)

def mouse_drag(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

def zoom(event):
    factor = 1.1 if event.delta > 0 else 0.9
    canvas.scale("all", event.x, event.y, factor, factor)

# -----------------------------------------
# INTERFACE GRÁFICA
# -----------------------------------------

root = tb.Window(themename="cyborg")
root.title("Warehouse Manager PRO")
root.geometry("1500x900")

frame_top = ttk.Frame(root)
frame_top.pack(fill=X, pady=10)

ttk.Label(frame_top, text="Adicionar local extra:", font=("Segoe UI", 10)).grid(row=0, column=0)
entry_local = ttk.Entry(frame_top, width=30)
entry_local.grid(row=0, column=1, padx=5)
ttk.Button(frame_top, text="Adicionar", command=adicionar_local_extra, bootstyle=SUCCESS).grid(row=0, column=2)

ttk.Label(frame_top, text="Excel SKUs:", font=("Segoe UI", 10)).grid(row=1, column=0)
entry_excel = ttk.Entry(frame_top, width=30)
entry_excel.grid(row=1, column=1, padx=5)
ttk.Button(frame_top, text="Importar Excel", command=importar_excel, bootstyle=INFO).grid(row=1, column=2)

ttk.Label(frame_top, text="Buscar SKU:", font=("Segoe UI", 10)).grid(row=2, column=0)
entry_sku = ttk.Entry(frame_top, width=30)
entry_sku.grid(row=2, column=1, padx=5)
ttk.Button(frame_top, text="Buscar", command=buscar_sku, bootstyle=PRIMARY).grid(row=2, column=2)

canvas = tk.Canvas(root, bg="#1a1a1a", scrollregion=(0, 0, 3000, 3000))
canvas.pack(fill=BOTH, expand=True)

canvas.bind("<ButtonPress-1>", mouse_press)
canvas.bind("<B1-Motion>", mouse_drag)
canvas.bind("<MouseWheel>", zoom)

desenhar_mapa()

root.mainloop()
