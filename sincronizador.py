import csv
import matplotlib.pyplot as plt
import scipy.signal as ss
import detect_clap


# Comprueba si NO esta en rango
def noEnRango(lista, num):
    RANGO = 20
    no_en_rango = True
    for i in lista:
        if (num > i-RANGO and num < i+RANGO):#si esta en rango
            no_en_rango = False
    return no_en_rango


def parser(fich):
    # PARSER
    left_acc_x = []
    left_acc_y = []
    left_acc_z = []

    frame = []

    #fich = input("introduce nombre fichero .csv:")
    #fich = fich+".csv"
    with open(fich) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # Pillamos los datos del acelerometro. Ver CSV, pos 1,2,3, asumimos xyz
            left_acc_x.append(abs(float(row[1])))
            left_acc_y.append(abs(float(row[2])))
            left_acc_z.append(abs(float(row[3])))
            frame.append(line_count)
            line_count += 1
    return line_count,left_acc_x,left_acc_y,left_acc_z,frame

def sincronizar_datos(csv_direccion,mp4_direccion):

    gyro_x = []
    gyro_y = []
    gyro_z = []

    right_acc_x = []
    right_acc_y = []
    right_acc_z = []

    line_count, left_acc_x, left_acc_y, left_acc_z,frame = parser(csv_direccion)

    # Calculamos los picos del ejex y se guardaran en picos_x y picos_plot_x para poder plotearlos
    UMBRAL = 100
    picos_x = ss.find_peaks(left_acc_x, UMBRAL, None, 50)
    picos_plot_x = []
    i = 1
    for z in left_acc_x:
        if (i in picos_x[0]):
            picos_plot_x.append(158)
        else:
            picos_plot_x.append(0)
        i = i + 1

    # Lo mismo del y, sorry x hardcodear pero hay prisa
    picos_y = ss.find_peaks(left_acc_y, UMBRAL, None, 50)
    picos_plot_y = []
    i = 1
    for z in left_acc_y:
        if (i in picos_y[0]):
            picos_plot_y.append(148)
        else:
            picos_plot_y.append(0)
        i = i + 1
    # lo mismo del z
    picos_z = ss.find_peaks(left_acc_z, UMBRAL, None, 50)
    picos_plot_z = []
    i = 1
    for z in left_acc_z:
        if (i in picos_z[0]):
            picos_plot_z.append(138)
        else:
            picos_plot_z.append(0)
        i = i + 1

    # Vamos a detectar donde hay picos, en cualquiera de los 3 ejes.
    # Damos margen de +-10 samples para asumir q es el mismo pico.
    picos = list(picos_x[0])

    for y in picos_y[0]:
        if (noEnRango(picos, y)):
            picos.append(y)
    # falta z
    for z in picos_z[0]:
        if (noEnRango(picos, z)):
            picos.append(z)
    picos.sort()
    picos_plot = []
    # generamos ploteble
    for i in range(0, line_count):
        if (i in picos):
            picos_plot.append(120)
        else:
            picos_plot.append(0)
        i = i + 1

    print(len(picos))
    print(picos)
    """
    plt.figure()
    plt.suptitle('lol')

    plt.plot(left_acc_x)  # plots de los valores de los accels
    plt.plot(left_acc_y)
    plt.plot(left_acc_z)

    plt.plot(picos_plot, marker='x')

    plt.plot(picos_plot_x, marker='x')  # Plots de detecciones individuales x eje
    plt.plot(picos_plot_y, marker='x')
    plt.plot(picos_plot_z, marker='x')

    plt.plot()
    plt.show()
    """
    # Variables de tiempo llamada a su funcion
    #path_wav=input("Intrudzca la direccion del video. (fichero mp4): ")
    tiempo_primera,tiempo_segunda,tiempo_tercera,tiempo_cuarta=detect_clap.procesar(mp4_direccion)
    
    video_synch_init = tiempo_segunda
    video_synch_end = tiempo_tercera  # ens segundos tiene que estar.

    best_candidate_begin = picos[1]  # el segundo de los picos
    best_candidate_end = picos[-2]  # el penultimo candidato
    sampling_rate=(best_candidate_end-best_candidate_begin)/(video_synch_end-video_synch_init)
    #sampling_rate=int(sampling_rate)
    print(sampling_rate)
    return video_synch_init,video_synch_end,best_candidate_begin,best_candidate_end,sampling_rate






