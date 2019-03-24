import sys
import matplotlib.pyplot as plt
import adidasSensor
from adidasSensor.sync import sync_video
import sincronizador
import re
import os

def get_dir_name(directorio):
    patron_mp4 = re.compile('.\.mp4')
    patron_csv=  re.compile('.\.csv')
    csv_direccion=""
    mp4_direccion=""
    for fichero in os.listdir(directorio):
        if patron_mp4.search(str(fichero)):
            mp4_direccion = "./"+directorio+"/"+str(fichero)
        if patron_csv.search(str(fichero)):
            csv_direccion = "./"+directorio+"/"+str(fichero)
    if csv_direccion==("./"+directorio+"/") or  mp4_direccion==("./"+directorio+"/"):
        print("introduzca un directorio con el csv y el mp4.")
        return 


    return csv_direccion,mp4_direccion



def getSyncedData(csv_file,video_synch_init,video_synch_end,best_candidate_end,best_candidate_begin,sampling_rate):
        synced = sync_video(
            csv_file=csv_file,
            best_candidate_begin=best_candidate_begin,
            best_candidate_end=best_candidate_end,
            video_synch_init=video_synch_init,
            video_synch_end=video_synch_end,
            sampling_rate=sampling_rate).values

        acc = synced[:, 0:3]
        gyr = synced[:, 3:6]
        time = synced[:, 6:7]


        return acc, gyr, time

def main():
    directorio = input("introduce nombre directorio  que contenga el csv y mp4: ")
    csv_direccion,mp4_direccion = get_dir_name(directorio)
    print(csv_direccion,mp4_direccion)
    video_synch_init,video_synch_end,best_candidate_begin,best_candidate_end,sampling_rate=sincronizador.sincronizar_datos(csv_direccion,mp4_direccion)
    #'./Prueba_6.csv'
    acc_raw, gyr_raw, time_raw = getSyncedData(csv_direccion,video_synch_init,video_synch_end,best_candidate_end,best_candidate_begin,sampling_rate)

    indexes = []

    times = []

    acc = []
    gyr = []
    time = []

    for index, (acc_value, gyr_value, time_value) in enumerate(zip(acc_raw, gyr_raw, time_raw)):
      if (time_value == 0):
        continue

      acc.append(acc_value)
      gyr.append(gyr_value)
      time.append(time_value)
    

    plt.figure()
    plt.suptitle('hack')

    ax1 = plt.subplot(211)
    plt.plot(time, acc)
    plt.ylabel('Linear acceleration [m/s^2]')

    ax2 = plt.subplot(212, sharex=ax1)
    plt.plot(time, gyr)
    plt.ylabel('Angular velocity [s]')

    plt.show()


if __name__ == "__main__":
    main()
