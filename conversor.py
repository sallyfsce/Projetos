import tkinter as tk
from tkinter import ttk

unidades = {
    "Comprimento": {
        "base": "metro",
        "fatores": {
            "metro": 1,
            "quilômetro": 1000,
            "milha": 1609.34,
            "centímetro": 0.01
        }
    },
    "Peso": {
        "base": "quilograma",
        "fatores": {
            "quilograma": 1,
            "grama": 0.001,
            "libra": 0.453592
        }
    }
}

categorias = list(unidades.keys()) + ["Temperatura"]

janela = tk.Tk()
janela.title("Conversor de Unidades")
janela.geometry("450x400")
janela.resizable(False, False)

janela.mainloop()

