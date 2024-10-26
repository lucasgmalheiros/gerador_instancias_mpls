import os
import csv
import re

def extract_numbers_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Remove any carriage returns for consistency
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        # Use regex to find all numbers in the file
        numbers = re.findall(r'[-+]?\d*\.\d+|\d+', content)
        # Convert extracted strings to floats or ints
        numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers

def comparar_arquivos_pastas(pasta1, pasta2, output_csv):
    arquivos_pasta1 = os.listdir(pasta1)
    arquivos_pasta2 = os.listdir(pasta2)
    
    arquivos_comuns = set(arquivos_pasta1) & set(arquivos_pasta2)

    resultados = []

    for arquivo in arquivos_comuns:
        caminho_arquivo1 = os.path.join(pasta1, arquivo)
        caminho_arquivo2 = os.path.join(pasta2, arquivo)
        
        try:
            numeros_arquivo1 = extract_numbers_from_file(caminho_arquivo1)
            numeros_arquivo2 = extract_numbers_from_file(caminho_arquivo2)
            
            iguais = numeros_arquivo1 == numeros_arquivo2
            if not iguais:
                # Optionally, you can check if the difference is negligible
                if len(numeros_arquivo1) == len(numeros_arquivo2):
                    diffs = [abs(a - b) for a, b in zip(numeros_arquivo1, numeros_arquivo2)]
                    max_diff = max(diffs)
                    # Define a tolerance level, e.g., 1e-6
                    tolerance = 1e-6
                    iguais = max_diff < tolerance
        except Exception as e:
            print(f"Erro ao comparar {arquivo}: {e}")
            iguais = False

        resultados.append([arquivo, iguais])

    # Salva os resultados em um arquivo CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Arquivo', 'Sao_Iguais'])  # Cabeçalhos
        writer.writerows(resultados)

    print(f"Resultados salvos em {output_csv}")

# Defina os caminhos das pastas e o arquivo de saída
pasta_c = 'instancias_c'
pasta_py = 'instancias_py_demand_adjust'
output_csv = 'comparacao_arquivos.csv'

# Chame a função para comparar os arquivos e salvar os resultados em CSV
comparar_arquivos_pastas(pasta_c, pasta_py, output_csv)
