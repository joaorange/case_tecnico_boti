import pandas as pd

# Função para carregamento das bases
def load_data(gcp_path, local_path):
    df_gcp = pd.read_csv(gcp_path, sep=',', dtype=str)
    df_local = pd.read_csv(local_path, sep=';', dtype=str)
    return df_gcp, df_local

# Realizando merge com base no ID
def merge_dataframes(df_local, df_gcp):
    df_merge = df_local.merge(df_gcp, on='ID', how='outer', indicator=True)
    return df_merge

# Verificando se o dataframe possue linhas duplicadas
def analyze_duplicates(df):
    return df.duplicated().value_counts()

# Gerando relatório com as informações do merge
def generate_report(df_merge):
    # Substituindo os valores do merge
    merge_counts = df_merge['_merge'].value_counts().rename(index={
        'left_only': 'local_only',
        'right_only': 'gcp_only',
        'both': 'both'
    })
    return {'merge_counts': merge_counts.to_dict()}

# Comparando o join entre os dataframes
def compare_dataframes(df_local, df_gcp):
    df_merge = merge_dataframes(df_local, df_gcp)


    report = generate_report(df_merge)

    df_both = df_merge[df_merge['_merge'] == 'both']
    df_both = df_both.drop(columns=['_merge'])
    df_both.columns = df_both.columns.str.replace('_x', '_LOCAL').str.replace('_y', '_GCP')

    # Comparando os valores de cada coluna
    resultados = {}
    for coluna in df_local.columns:
        if coluna != 'ID':
            diferentes = df_both[coluna + '_LOCAL'] != df_both[coluna + '_GCP']
            quantidade_diferencas = diferentes.sum()

            if quantidade_diferencas > 0:
                exemplos_diferencas = df_both[diferentes][
                    ['ID', coluna + '_LOCAL', coluna + '_GCP']].head()
                resultados[coluna] = {
                    'quantidade': quantidade_diferencas,
                    'exemplos': exemplos_diferencas
                }

    return report, resultados

# Salvando todas as informações em um TXT
def save_report_to_txt(report, resultados, gcp_duplicates, local_duplicates):
    with open("report.txt", "w") as f:
        f.write("### Report ###\n")
        f.write("Merge Counts:\n")
        for key, value in report['merge_counts'].items():
            f.write(f"{key}: {value}\n")

        f.write("\n### Duplicados GCP ###\n")
        f.write(str(gcp_duplicates) + "\n")

        f.write("\n### Duplicados Local ###\n")
        f.write(str(local_duplicates) + "\n")

        f.write("\n### Diferenças ###\n")
        for coluna, info in resultados.items():
            f.write(f"Coluna: {coluna}, Quantidade de Diferenças: {info['quantidade']}\n")
            f.write("Exemplos de Diferenças:\n")
            f.write(info['exemplos'].to_string(index=False) + "\n")
            f.write("\n")


def main():
    gcp_path = 'C:/Users/JoaoV/OneDrive/Área de Trabalho/case_2024/bases/application_record_gcp.csv'
    local_path = 'C:/Users/JoaoV/OneDrive/Área de Trabalho/case_2024/bases/application_record_local.csv'

    df_gcp, df_local = load_data(gcp_path, local_path)

    report, resultados = compare_dataframes(df_local, df_gcp)

    # Analisando duplicados
    gcp_duplicates = analyze_duplicates(df_gcp)
    local_duplicates = analyze_duplicates(df_local)

    # Salvando o relatório em um txt
    save_report_to_txt(report, resultados, gcp_duplicates, local_duplicates)


if __name__ == "__main__":
    main()
