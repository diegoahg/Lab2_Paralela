
import re
import random
import os


def keywordList():

    # Abrir ficheros
    #currentDir = os.path.dirname(os.path.abspath(__file__))
    path = "/mpi/BIBLIA/Diccionarios/"
    archivo_apocalipsis = open(path + 'apocalipsis.txt', 'r')
    archivo_apellidos=open(path+'apellidos.txt', 'r')
    archivo_marca=open(path+'marca.txt', 'r')
    archivo_moda=open(path+'moda.txt', 'r')
    archivo_nombres=open(path+'nombres.txt', 'r')
    archivo_actualidad=open(path+'actualidad.txt', 'r')
    archivo_animales=open(path+'animales.txt', 'r')
    archivo_enfermedades=open(path+'enfermedades.txt', 'r')
    archivo_paises=open(path+'paises.txt', 'r')
    archivo_verbos=open(path+'verbos.txt', 'r')


# Listas que almacenarán las palabras de los diccionarios

    lista = []

    # Lectura de ficheros
    """
    # Lista Nombres
    for linea in archivo_nombre:
        lista.append(re.sub("[^a-z]","",linea))
    # Lista Países
    for linea in archivo_paises:
        lista.append(re.sub("[^a-z]","",linea))
    # Lista Verbos
    for linea in archivo_verbos:
        lista.append(re.sub("[^a-z]","",linea))
    """
    # Lista Cosas
    for linea in archivo_apocalipsis:
        lista.append(re.sub("[^a-z]", "", linea))
    for linea in archivo_apellidos:
        lista.append(re.sub("[^a-z]","",linea))
    for linea in archivo_marca:
        lista.append(re.sub("[^a-z]","",linea))    
    for linea in archivo_moda:
        lista.append(re.sub("[^a-z]","",linea))
    for linea in archivo_nombres:
        lista.append(re.sub("[^a-z]","",linea))
    for linea in archivo_actualidad:
        lista.append(re.sub("[^a-z]","",linea))    
    for linea in archivo_animales:
        lista.append(re.sub("[^a-z]","",linea))
    for linea in archivo_enfermedades:
        lista.append(re.sub("[^a-z]","",linea))
    for linea in archivo_paises:
        lista.append(re.sub("[^a-z]","",linea))
    for linea in archivo_verbos:
        lista.append(re.sub("[^a-z]","",linea))   


    # Cierre de ficheros.
    archivo_apocalipsis.close()
    archivo_nombres.close()
    archivo_marca.close()
    archivo_moda.close()
    archivo_apellidos.close()
    archivo_verbos.close()
    archivo_animales.close()
    archivo_enfermedades.close()
    archivo_paises.close()
    archivo_actualidad.close()


    return lista
