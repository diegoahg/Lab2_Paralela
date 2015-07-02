# -*- coding: utf-8 -*-

import subprocess
import re
import codecs

from PyPDF2 import PdfFileReader


def toStringFormat(path):
    # tiempo inicial
    # se inicia la cadena que almacenará el contenido de cada página
    # del pdf
    contenido_pagina = ""
    # instanciando lista a ocupar
    lista = list()
    # abrir pdf en modo lectura
    pdf = PdfFileReader(codecs.open(path, "rb"))
    # imprime cuantas páginas tiene el pdf:
    numero_paginas = pdf.getNumPages()
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
        contenido_pagina = codecs.open(txt, encoding='ISO-8859-1').read().lower()
        contenido_pagina = contenido_pagina.replace('á', 'a')
        contenido_pagina = contenido_pagina.replace('é', 'e')
        contenido_pagina = contenido_pagina.replace('í', 'i')
        contenido_pagina = contenido_pagina.replace('ó', 'o')
        contenido_pagina = contenido_pagina.replace('ú', 'u')
        contenido_pagina = contenido_pagina.replace('ñ', 'n')
        contenido_pagina = re.sub('[^a-z]', '', contenido_pagina)
        lista.append(contenido_pagina)
        subprocess.call("rm -R " + txt, shell=True)
        

    return lista
