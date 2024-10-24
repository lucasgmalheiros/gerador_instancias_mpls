import os
import csv

def comparar_arquivos_pastas(pasta1, pasta2, output_csv):
    arquivos_pasta1 = os.listdir(pasta1)
    arquivos_pasta2 = os.listdir(pasta2)
    
    arquivos_comuns = set(arquivos_pasta1) & set(arquivos_pasta2)

    resultados = []

    for arquivo in arquivos_comuns:
        caminho_arquivo1 = os.path.join(pasta1, arquivo)
        caminho_arquivo2 = os.path.join(pasta2, arquivo)
        
        with open(caminho_arquivo1, 'r') as f1, open(caminho_arquivo2, 'r') as f2:
            conteudo_arquivo1 = f1.read()
            conteudo_arquivo2 = f2.read()
            
            iguais = conteudo_arquivo1 == conteudo_arquivo2
            resultados.append([arquivo, iguais])

    # Salva os resultados em um arquivo CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Arquivo', 'Sao_Iguais'])  # Cabeçalhos
        writer.writerows(resultados)

    print(f"Resultados salvos em {output_csv}")

# Defina os caminhos das pastas e o arquivo de saída
pasta_c = 'instancias_c'
pasta_py = 'instancias_py'
output_csv = 'comparacao_arquivos.csv'

# Chame a função para comparar os arquivos e salvar os resultados em CSV
comparar_arquivos_pastas(pasta_c, pasta_py, output_csv)
