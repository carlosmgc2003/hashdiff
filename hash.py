import os
import cv2
from time import time



#Calcula el hash de la imagen y guarda una copia redimensionada
def dhash(imagen, nombre, hashSize = 8):
    # redimensionar la imagen de entraada agregando una sola columna
    # Asi podemos calcular el gradiente horizonal
    redimensionada = cv2.resize(imagen, (hashSize + 1, hashSize))

    # Computar el gradiente (relativo) horizontal
    gradiente = redimensionada[:, 1:] > redimensionada[:, :-1]
    cv2.imwrite('./salida/' + nombre,redimensionada)
    return sum([2 ** i for (i, v) in enumerate(gradiente.flatten()) if v])

#Halla todos los archivos y devuelve un diccionario cuya clave es el nombre
#de archivo y su valor es la ruta
def hallarArchivos(ruta) -> dict:
    archivos = {}
    for base, _, archs in os.walk(ruta):
        for nombre in archs:
            archivos[nombre] = os.path.join(base,nombre)
    return archivos

#Halla valores duplicados en un diccionario
def hallarDuplicados(dictHashes : dict) -> dict:
    invertido = {}
    for clave, valor in dictHashes.items():
        if valor not in invertido:
            invertido[valor] = [clave]
        else:
            invertido[valor].append(clave)
    return invertido

if __name__ == "__main__":
    tiempo_inicial = time()
    resultados = {}

    for archivo,ruta in hallarArchivos('/Volumes/maceira/fotos').items():
        imagen = cv2.imread(ruta)
        if imagen is None:
            continue

        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        resultados[archivo] = dhash(imagen, archivo)

    duplicados = hallarDuplicados(resultados)

#Guardar un archivo de texto con los resultados
    with open('./salida.txt',mode='w') as archivo_salida:
        for clave, valor in duplicados.items():
            archivo_salida.write('{}: {}\n'.format(clave, valor))

    tiempo_final = time()
    print('El tiempo de ejecucion fue: {}'.format(tiempo_final - tiempo_inicial))