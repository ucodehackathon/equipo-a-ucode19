import os
from scipy.io.wavfile import read
import numpy as np
import math
import subprocess
import matplotlib.pyplot as plt


def procesar(path_to_video):
    path_to_wav=procesar_video(path_to_video)
    print('Inicio')# Leer wav y freq de muestreo
    audio = read(path_to_wav)
    audio_array = np.array(audio[1][:,0],dtype=float)
    len_audio = np.shape(audio_array)[0]
    audio_array = np.reshape(audio_array,(len_audio, 1))
    # audio_array = audio_array/max(audio_array)
    freq = audio[0]
    plt.plot(audio_array)
    plt.show()
    #print('Len: ',len_audio,len_audio/(freq),'s,','Freq:',freq)

    #Ventana
    window_time = .01
    batch = int(window_time*freq)
    #print('Windows',window_time,'s, Batch:',batch)

    num_windows = 40 #Ventanas iniciales para calcular la media e potencia
    cont = 0
    power, potencias = [], []
    power_maxs = []
    pot_anterior = .00001
    x = 2
    for i in range(0,len_audio,batch):
        pot = potencia(audio_array[i:i+batch])
        mean_ventana = np.mean(sum(audio_array[i:i+batch]))
        index, maxo = maximo(audio_array[i:i+batch])
        #nou = maxo/mean_ventana
        if cont < num_windows:
            power.append(pot)
            cont += 1
        else: #Añadir parametros
            pot_mean = np.mean(power)
            if pot > x*pot_mean:
                index, maxe = maximo(audio_array[i:i+batch])
                tmp = []
                tmp.append(index)
                tmp.append(maxe)
                potencias.append(pot)
                tmp.append((i+index)/freq)
                tmp.append(pot)
                power_maxs.append(tmp)
        #         if pot/pot_anterior > 0.001:
        #             print(tmp)
        # pot_anterior = pot

    # plt.plot(power+potencias)
    # plt.ylabel('Pot')
    # plt.show()

    # print(pot_mean)
    #print(power_maxs)
    s = sorted(power_maxs, key=lambda x: x[1])
    #print(s)
    #print(s[-4:])
    max_four = s[-4:]
    #Sort by time
    s = sorted(max_four,key=lambda x: x[2])
    #print("Final 4 palamadas:", s)
    tiempo_primera = s[0][2]
    tiempo_segunda = s[1][2]
    tiempo_tercera = s[2][2]
    tiempo_cuarta = s[3][2]
    print("Tiempos: ",tiempo_primera,tiempo_segunda,tiempo_tercera,tiempo_cuarta)
    return tiempo_primera,tiempo_segunda,tiempo_tercera,tiempo_cuarta




def maximo(vector):
    return np.argmax(vector), np.max(vector)

def potencia(wave):
    res = sum(wave**2)/len(wave)
    if res ==0:
        res = .00001
    return math.log10(res)*10


def procesar_video(path_video):

    #path_video = r"D:\uCode\dos_palmas_final_inicio.mp4"
    name = os.path.split(path_video)[-1].replace('.mp4','.wav')
    if not os.path.exists(name):
        command = "ffmpeg -i "+path_video+" -ab 160k -ac 2 -ar 44100 -vn "+name
        subprocess.call(command, shell=True)

    return name