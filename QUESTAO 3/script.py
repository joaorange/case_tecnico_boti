import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

# Lendo o CSV
def read_csv(caminho, sep, decimal='.'):
    return pd.read_csv(caminho, sep=sep, decimal=decimal)

# Transformando a coluna "target" em valores de "1" e "0"
def event_nonevent(df, coluna_evento, evento, nao_evento):
    df = df.copy()
    df[coluna_evento] = df[coluna_evento].apply(lambda x: 1 if x == evento else (0 if x == nao_evento else x))
    return df

# Gráfico para visualização da curva de KS
def graph_ks(df, coluna_evento, coluna_probabilidade, evento, nao_evento):
    score_0 = df[df[coluna_evento] == 0][coluna_probabilidade]
    score_1 = df[df[coluna_evento] == 1][coluna_probabilidade]

    x_0 = np.sort(score_0)
    y_0 = np.arange(1, len(x_0) + 1) / len(x_0)

    x_1 = np.sort(score_1)
    y_1 = np.arange(1, len(x_1) + 1) / len(x_1)

    x_all = np.sort(np.concatenate((x_0, x_1)))
    y_0_interp = np.searchsorted(x_0, x_all, side='right') / len(x_0)
    y_1_interp = np.searchsorted(x_1, x_all, side='right') / len(x_1)
    difference = np.abs(y_0_interp - y_1_interp)

    ks_statistic = np.max(difference)
    ks_index = np.argmax(difference)
    ks_x_value = x_all[ks_index]
    ks_y_value = y_0_interp[ks_index]

    plt.figure(figsize=(10, 6))
    plt.plot(x_0, y_0, marker='o', label=nao_evento, linestyle='-', color='blue')
    plt.plot(x_1, y_1, marker='o', label=evento, linestyle='-', color='orange')

    plt.annotate(f'KS = {ks_statistic:.2f}', xy=(ks_x_value, ks_y_value),
                 xytext=(ks_x_value + 0.1, ks_y_value - 0.1),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    plt.title('Distribuição Acumulada dos Scores por Classe com KS')
    plt.xlabel('SCORE')
    plt.ylabel('Fração Acumulada')
    plt.legend()
    plt.grid()
    plt.show()

# Processando o CSV com base nas entradas do tkinter
def process_csv(sep_entry, decimal_entry, coluna_evento_entry, coluna_probabilidade_entry, evento_entry, nao_evento_entry):
    caminho_csv = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=[("CSV files", "*.csv")])
    if not caminho_csv:
        return

    sep = sep_entry.get()
    decimal = decimal_entry.get() if decimal_entry.get() else '.'
    coluna_evento = coluna_evento_entry.get()
    coluna_probabilidade = coluna_probabilidade_entry.get()
    evento = evento_entry.get()
    nao_evento = nao_evento_entry.get()

    try:
        df = read_csv(caminho_csv, sep, decimal)
        df = event_nonevent(df, coluna_evento, evento, nao_evento)
        graph_ks(df, coluna_evento, coluna_probabilidade, evento, nao_evento)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Criando o software
def create_gui():
    root = tk.Tk()
    root.title("Análise KS")

    tk.Label(root, text="Separador do CSV (por exemplo, ';'):").grid(row=0, column=0)
    sep_entry = tk.Entry(root)
    sep_entry.grid(row=0, column=1)

    tk.Label(root, text="Decimal, se houver (o default é '.'):").grid(row=1, column=0)
    decimal_entry = tk.Entry(root)
    decimal_entry.grid(row=1, column=1)

    tk.Label(root, text="Coluna de Evento:").grid(row=2, column=0)
    coluna_evento_entry = tk.Entry(root)
    coluna_evento_entry.grid(row=2, column=1)

    tk.Label(root, text="Coluna de Probabilidade:").grid(row=3, column=0)
    coluna_probabilidade_entry = tk.Entry(root)
    coluna_probabilidade_entry.grid(row=3, column=1)

    tk.Label(root, text="Valor do Evento:").grid(row=4, column=0)
    evento_entry = tk.Entry(root)
    evento_entry.grid(row=4, column=1)

    tk.Label(root, text="Valor do Não Evento:").grid(row=5, column=0)
    nao_evento_entry = tk.Entry(root)
    nao_evento_entry.grid(row=5, column=1)

    tk.Button(root, text="Selecionar CSV e Gerar Gráfico", command=lambda: process_csv(
        sep_entry, decimal_entry, coluna_evento_entry, coluna_probabilidade_entry, evento_entry, nao_evento_entry
    )).grid(row=6, columnspan=2)

    root.mainloop()

def main():
    create_gui()

if __name__ == "__main__":
    main()
