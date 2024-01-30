import os
import scipy.signal as signal
from scipy.io import wavfile
import shutil

# Diretório atual (onde estão os arquivos FLAC e subdiretórios)
diretorio_atual = os.getcwd()

# Frequência de corte do filtro passa-baixa
cutoff_freq = 25000  # Hz

# Percorra todos os arquivos no diretório atual e subdiretórios
for root, _, filenames in os.walk(diretorio_atual):
    for nome_arquivo in filenames:
        if nome_arquivo.lower().endswith(".flac"):
            # Caminho completo do arquivo
            caminho_completo = os.path.join(root, nome_arquivo)

            # Carregue o arquivo FLAC
            fs, audio_data = wavfile.read(caminho_completo)

            # Projete o filtro passa-baixa
            nyquist_freq = 0.5 * fs
            b, a = signal.butter(4, cutoff_freq / nyquist_freq, btype='low')

            # Aplique o filtro
            filtered_audio = signal.lfilter(b, a, audio_data)

            # Salve o arquivo filtrado temporariamente
            temp_filename = f"{nome_arquivo}_temp.flac"
            wavfile.write(temp_filename, fs, filtered_audio)

            # Copie os metadados do arquivo original para o novo arquivo
            shutil.copy2(caminho_completo, temp_filename)

            # Renomeie o novo arquivo para o nome do arquivo original
            os.rename(temp_filename, caminho_completo)

print("Filtros aplicados, arquivos substituídos e metadados preservados com sucesso!")
