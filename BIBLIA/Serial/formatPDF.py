# -*- coding: utf-8 -*-

import subprocess
import re

from PyPDF2 import PdfFileReader


def toStringFormat(path):
    # tiempo inicial
    # se inicia la cadena que almacenará el contenido de cada página
    # del pdf
    contenido_pagina = ""
    # instanciando lista a ocupar
    lista = list()
    # abrir pdf en modo lectura
    pdf = PdfFileReader(open(path, "rb"))
    # imprime cuantas páginas tiene el pdf:
    numero_paginas = pdf.getNumPages() # pdf.getOutlines
    # print("Numero de paginas del PDF: ", numero_paginas)
    # uso de la librería PyPDF2 para obtener la cantidad de hojas del pdf
    for i in range(numero_paginas):
        # convierte página i de pdf en txt
        subprocess.call(
            "pdftotext -f " + str(i + 1) + " -l " + str(i + 1) +
            " " + path, shell=True)
        # reemplazo de .pdf a .txt en path
        txt = path.replace(".pdf", ".txt")
        # abrir fichero txt que trae el contenido de la página i del pdf +
        # limpieza del string
        contenido_pagina = open(txt).read().lower()
        contenido_pagina = contenido_pagina.replace('á', 'a')
        contenido_pagina = contenido_pagina.replace('é', 'e')
        contenido_pagina = contenido_pagina.replace('í', 'i')
        contenido_pagina = contenido_pagina.replace('ó', 'o')
        contenido_pagina = contenido_pagina.replace('ú', 'u')
        contenido_pagina = contenido_pagina.replace('ñ', 'n')
        contenido_pagina = re.sub('[^a-z]', '', contenido_pagina)
        lista.append(contenido_pagina)
        # subprocess.call("rm -R " + txt, shell=True)

    return lista

def toStringFormatParalell(path, rank, size, comm):

    pdf = PdfFileReader(open(path, "rb"))    
    numero_paginas = pdf.getNumPages()
    print("******************************************",numero_paginas)

    intervalo = int(numero_paginas/size)
    resto = numero_paginas%size
    fin, inicio = 0, 0

    if(rank==0):

        for i in range(1, size):

            if(i == rank):
                fin += intervalo
                inicio = (fin - intervalo) + 1
                fin += resto
                data = {'inicio':inicio, 'fin': fin, 'path': path}
                comm.send(data, dest=i, tag=1)

            else:

                fin += intervalo
                inicio = (fin - intervalo) + 1
                data = {'inicio':inicio, 'fin': fin, 'path': path}
                comm.send(data, dest=i, tag=1)

    if(rank!=0):

        data = comm.recv(source=0, tag=1)
        contenido_pagina = ""
        lista = list()
        for i in range(data['inicio'], data['fin']):

            txt = data['path'].replace(".pdf", rank + ".txt")

            subprocess.call(
            "pdftotext -f " + str(i + 1) + " -l " + str(i + 1) +
            " " + data['path'], shell=True)

            contenido_pagina = open(txt).read().lower()
            contenido_pagina = contenido_pagina.replace('á', 'a')
            contenido_pagina = contenido_pagina.replace('é', 'e')
            contenido_pagina = contenido_pagina.replace('í', 'i')
            contenido_pagina = contenido_pagina.replace('ó', 'o')
            contenido_pagina = contenido_pagina.replace('ú', 'u')
            contenido_pagina = contenido_pagina.replace('ñ', 'n')
            contenido_pagina = re.sub('[^a-z]', '', contenido_pagina)
            lista.append(contenido_pagina)
            #subprocess.call("rm -R " + txt, shell=True)

        comm.send(lista, dest=0, tag=2)

    if(rank == 0):
        book = []
        for i in range(1,size):
            book += comm.recv(source=i, tag=2)

        return book












    

