import os
import csv
import shutil

# Diretório onde deseja criar as pastas e arquivos CSV
diretorio_origem = 'C:\\facul\IC\\teste'
# Diretório onde estão os arquivos a serem copiados
diretorio_destino = 'C:\\facul\IC\\teste2'

# Nomes das pastas armazenados em um objeto (lista, no exemplo)
nomes_pastas = ['pasta1', 'pasta2']

#contador para os ids dos arquivos
contador = 0

# Dados a serem armazenados nos arquivos CSV (substitua isso pelo seu próprio conjunto de dados)
dados_para_csv = {
    'pasta1': ['linha1', 'linha2', 'linha3'],
    'pasta2': ['dados1', 'dados2', 'dados3'],
}

# Iterar sobre as pastas
for nome_pasta in nomes_pastas:
    # Caminho completo para a pasta
    caminho_pasta_destino = os.path.join(diretorio_destino, nome_pasta)
    
    # Verificar se a pasta de origem existe
    if os.path.exists(diretorio_origem):
        # Verificar se a pasta de destino já existe
        if not os.path.exists(caminho_pasta_destino):
            os.makedirs(caminho_pasta_destino)
            print(f"Pasta '{nome_pasta}' criada em '{diretorio_destino}'.")
        
            # Copiar arquivos PNG da pasta de origem para a pasta de destino
            for arquivo_origem in os.listdir(diretorio_origem):
                if arquivo_origem.lower().endswith('.png'):
                    caminho_arquivo_origem = os.path.join(diretorio_origem, arquivo_origem)
                    caminho_arquivo_destino = os.path.join(caminho_pasta_destino, f'id{contador}.png')
                    
                    shutil.copy(caminho_arquivo_origem, caminho_arquivo_destino)
                    print(f"Arquivo '{arquivo_origem}' copiado como 'id{contador}.png'.")
                    
                    contador += 1
            
            # Criar e escrever dados no arquivo CSV
            caminho_arquivo_csv = os.path.join(caminho_pasta_destino, f'{nome_pasta}.csv')
            with open(caminho_arquivo_csv, 'w', newline='') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv)
                escritor_csv.writerow(['Dados'])  # Cabeçalho
                escritor_csv.writerows([linha] for linha in dados_para_csv.get(nome_pasta, []))
                
            print(f"Arquivo CSV criado em '{caminho_arquivo_csv}'.")
        else:
            print(f"Pasta '{nome_pasta}' já existe em '{diretorio_destino}'.")    
    else:
        print(f"Pasta '{diretorio_origem}' não existe.")


"""
criar executavel do codigo da interface grafica
    1 - instalar biblioteca pyinstaller
    2 - executar o comando no terminal: pyinstaller --windowed gui.py 

obs: o executavel fica na pasta dist, o pyinstaller compila apenas o codigo da interface, no caso o gui.py, todos os demais
codigos e imagens devem estar na mesma pasta do executavel para que ele funcione corretamente, então é necessario fazer uma
copia deles para a pasta dist.

"""