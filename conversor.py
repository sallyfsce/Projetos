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

quadro = tk.Frame(janela, padx=30, pady=20)
quadro.pack(expand=True, fill="both")

titulo = tk.Label(quadro, text="Conversor de Unidades", font=("Segoe UI", 16, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

ttk.Label(quadro, text="Categoria:").grid(row=1, column=0, sticky="w", pady=8)
combo_categoria = ttk.Combobox(quadro, values=categorias, state="readonly")
combo_categoria.grid(row=1, column=1, pady=8, sticky="ew")
combo_categoria.current(0)

ttk.Label(quadro, text="De:").grid(row=2, column=0, sticky="w", pady=8)
combo_de = ttk.Combobox(quadro, state="readonly")
combo_de.grid(row=2, column=1, pady=8, sticky="ew")

ttk.Label(quadro, text="Para:").grid(row=3, column=0, sticky="w", pady=8)
combo_para = ttk.Combobox(quadro, state="readonly")
combo_para.grid(row=3, column=1, pady=8, sticky="ew")

ttk.Label(quadro, text="Valor:").grid(row=4, column=0, sticky="w", pady=8)
entrada_valor = ttk.Entry(quadro, font=("Segoe UI", 11))
entrada_valor.grid(row=4, column=1, pady=8, sticky="ew")

quadro.columnconfigure(1, weight=1)

label_resultado = tk.Label(quadro, text="Resultado: ", font=("Segoe UI", 13, "bold"))
label_resultado.grid(row=6, column=0, columnspan=2, pady=10)

def atualizar_unidades(event=None):
    categoria = combo_categoria.get()

    if categoria == "Temperatura":
        opcoes = ["Celsius", "Fahrenheit", "Kelvin"]
    else:
        opcoes = list(unidades[categoria]["fatores"].keys())

    combo_de["values"] = opcoes
    combo_para["values"] = opcoes
    combo_de.current(0)
    combo_para.current(0)


combo_categoria.bind("<<ComboboxSelected>>", atualizar_unidades)
atualizar_unidades()


def converter():
    categoria = combo_categoria.get()
    unidade_de = combo_de.get()
    unidade_para = combo_para.get()

    try:
        valor = float(entrada_valor.get())
    except ValueError:
        label_resultado.config(text="Resultado: valor inválido")
        return

    if categoria == "Temperatura":
        if unidade_de == "Fahrenheit":
            celsius = (valor - 32) * 5 / 9
        elif unidade_de == "Kelvin":
            celsius = valor - 273.15
        else:
            celsius = valor

        if unidade_para == "Fahrenheit":
            resultado = celsius * 9 / 5 + 32
        elif unidade_para == "Kelvin":
            resultado = celsius + 273.15
        else:
            resultado = celsius
    else:
        fatores = unidades[categoria]["fatores"]
        valor_em_base = valor * fatores[unidade_de]
        resultado = valor_em_base / fatores[unidade_para]

    label_resultado.config(text=f"Resultado: {resultado:.2f}")


botao = ttk.Button(quadro, text="Converter", command=converter)
botao.grid(row=5, column=0, columnspan=2, pady=(20, 10))

janela.mainloop()

