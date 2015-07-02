# from formatPDF import toStringFormatParalell
from mpi4py import MPI
import subprocess
import re
from PyPDF2 import PdfFileReader
from numpy import *

import warnings
warnings.filterwarnings('ignore')

path = "niebla.pdf"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()




def toStringFormatParalell():
    book = []
    pdf = PdfFileReader(open(path, "rb"))
    numero_paginas = pdf.getNumPages()
    
    intervalo = int(numero_paginas / (size - 1))
    resto = numero_paginas % (size - 1)
    fin, inicio = 0, 0
    if(rank == 0):

        for i in range(1, size):

            if(i == size):
                fin += intervalo
                inicio = (fin - intervalo) + 1
                fin += resto
                data = {'inicio': inicio, 'fin': fin, 'path': path}
                comm.send(data, dest=i)

            else:

                fin += intervalo
                inicio = (fin - intervalo) + 1
                data = {'inicio': inicio, 'fin': fin, 'path': path}
                comm.send(data, dest=i)

    if(rank != 0):

        data = comm.recv(source=0)
        contenido_pagina = ""
        lista = list()
        for i in range(data['inicio'], data['fin']):

        	texto = data['path'].replace(".pdf", "")
        	archivo = texto + str(rank)
        	subprocess.call(
        	    "pdftotext -f " + str(i + 1) + " -l " + str(i + 1) + " " + data['path'] +" "+archivo+".txt", shell=True)

        	txt = archivo + ".txt"
        	contenido_pagina = open(txt).read().lower()
        	contenido_pagina = contenido_pagina.replace('á', 'a')
        	contenido_pagina = contenido_pagina.replace('é', 'e')
        	contenido_pagina = contenido_pagina.replace('í', 'i')
        	contenido_pagina = contenido_pagina.replace('ó', 'o')
        	contenido_pagina = contenido_pagina.replace('ú', 'u')
        	contenido_pagina = contenido_pagina.replace('ñ', 'n')
        	contenido_pagina = re.sub('[^a-z]', '', contenido_pagina)
        	lista.append(contenido_pagina)
        	subprocess.call("rm -R " + txt, shell=True)

        comm.send(lista, dest=0)

    if(rank == 0):

        for i in range(1,size):

        	if(i == 1):
        		book = comm.recv(source=i)
        	else:
        		book += comm.recv(source=i)
        
        return "hola"



entero = toStringFormatParalell()

print(entero)