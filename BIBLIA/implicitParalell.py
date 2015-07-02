# Se incluyen las funciones desarrolladas del codigo secuencial
from Paralelo.formatPDF import toStringFormat
from Paralelo.searchMatches import buscaPatron
from Paralelo.saltoProcesador import saltoProc
from Paralelo.elimRep import elimina_rep
from Paralelo.mail import envio_mail_paralelo_implicito
from dictionary import keywordList
from mpi4py import MPI
from numpy import *
from time import *
import sys
import json

# Se incluyen modulos para sacar Advertencias (warnings)
import warnings
warnings.filterwarnings('ignore')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()

procesadores = size
gtime = time()


def run():

    if(rank == 0):
        from pdf import crearPDF
        pdf = str(sys.argv[1])
        direccion = "/mpi/BIBLIA/Serial/" + pdf + ".pdf"
        txt = toStringFormat(direccion)

        keyword = keywordList()
        jumpMax = int(sys.argv[2])
        email = str(sys.argv[3])
        documento = str(sys.argv[4])

        start = time()

        keyword = keyword + [w[::-1] for w in keyword]

        print("largo de arreglo a buscar: ", len(keyword))


        # Calcula los saltos segun el salto maximo y la cantidad de
        # procesadores en una lista
        lsaltos = saltoProc(jumpMax, procesadores - 1)

        print(lsaltos)

        # Estima el tiempo antes de enviar datos a nodos esclavos
        trans = time() - start

        # Distribucion de carga en los nodos esclavos
        # Se envia a cada nodo la palabra, el documento como texto,
        # y el salto minimo y maximo.
        for i in range(1, procesadores):
            datos = {"minimo": lsaltos[(i * 2) - 2],
                     "maximo": lsaltos[(i * 2) - 1],
                     "texto": txt,
                     "palabra": keyword}
            # Se envia la lista de variables al nodo con rank i
            # print("<ENVIANDO>: Hacia procesador ",i," el salto [", lsaltos[(i * 2) - 2], "->", lsaltos[(i * 2) - 1],"]")
            comm.send(datos, dest=i, tag=1)

    if(rank != 0):
        # Recepcion de parametros desde el nodo maestro
        datos = comm.recv(source=0, tag=1)
        match = []
        # Establece el tiempo inicial
        start2 = time()

        # Asignacion de valores
        jumpMin = datos["minimo"]
        jumpMax = datos["maximo"]
        txt = datos["texto"]
        keyword = datos["palabra"]

        print("nodo ",name,rank, " recibe [",jumpMin,",",jumpMax,"]")

        # print("<EJECUTANDO>: Esclavo ",
        # name, ", Procesador Nro ", rank, "salto [", jumpMin, "->",
        # jumpMax,"]")

        # Busca las coincidencias con la keyword normal.

        # Busca las coincidencias con la keyword leida al reves.

        for i in range(len(keyword)):
            # Busca las coincidencias con la keyword leida al reves.
            match += buscaPatron(txt, keyword[i], jumpMin, jumpMax)

        # Calcula el tiempo final del nodo esclavo
        trans2 = time() - start2

        # Envio de Respuestas a nodo Maestro
        comm.send(match, dest=0, tag=1)
        comm.send(trans2, dest=0, tag=3)

        print("nodo ",name,rank, " envia [",len(match),"] enc.")


    if(rank == 0):
        match = []
        tiempo_min_sl = 9999
        start3 = time()

        toolbar_width = 50
        aux = (procesadores - 1) / toolbar_width
        cont = aux
        # print("\nBuscando...")
        # print("----------------------------------------------------------")
        # sys.stdout.write("0 [%s] 100" % (" " * (toolbar_width)))
        # sys.stdout.flush()

        # return to start of line, after '['
        # sys.stdout.write("\b" * (toolbar_width + 1 + 4))

        # Recepcion de parametros desde los nodos esclavos
        for i in range(1, procesadores):
            match += comm.recv(source=i, tag=1)
            print ("Se recibe desde nodo ",i)

            if(procesadores + 1 >= cont):
                # sys.stdout.write("#")
                # sys.stdout.flush()
                cont += aux

            # Recibe y estima el mayor tiempo de ejecucion en los esclavos
            tiempo = comm.recv(source=i, tag=3)
            if (tiempo < tiempo_min_sl):
                tiempo_min_sl = tiempo

            # print("< RECIBIENDO>: Respuesta desde procesador ", i, "en ", name,"[",rank,"]")
        # if(toolbar_width > (procesadores - 1)):
        #     for i in range(toolbar_width - (procesadores - 1)):
                # sys.stdout.write("#")
                # sys.stdout.flush()
        # sys.stdout.write("\n")
        print("Terminado de recibir. Empezando a eliminiar")
        # Calculo final de metricas
        trans3 = time() - start3
        total_time = trans + trans3  # + tiempo_min_sl

        # Eliminar resultados repetidos
        # match = elimina_rep(match)
        # match = elimina_rep(match)
        print("Eliminado lo repetidos")

        # Se establece si hubo cohincidencias o no, y muestra los resultados
        # segun corresponda
        if (len(match) == 0):
            print("Recopilacion Final Nodo ", name, "[", rank, "].")
            print(
                "*******************************************************************************\n")
            print("\tResultado Final : NO SE ENCONTRO LA PALABRA")
        else:
            print("")
            print("Recopilacion Final Nodo ", name, "[", rank, "].")
            print(
                "\n***********************************ENORDEN***********************************\n")
            # for i in range(len(datos)):
            #     print(datos[i])
            print(
                "\n*****************************************************************************\n")
            print("\tResultado Final ", len(match), ".")
            print(
                "\n*****************************************************************************\n")
        print("\tEn recorrer ", len(txt),
              " paginas. Salto Maximo: ", jumpMax, ".")
        print("\tT(e): ", round(total_time, 3), " segundos.")
        print("\tT(c): ", round(
            round(time() - gtime, 3) - round(total_time, 3), 3), " segundos.")
        print("\tT(t): ", round(time() - gtime, 3), " segundos.")
        print(
            "\n*****************************************************************************\n")
        tiempo_final = round(total_time, 3)

        prim_pag_o = 1  # json.loads('["dato":'+match[0]+']')

        # Estadisticas pdf
        abc = "abcdefghijklmnopqrstuvwxyz"
        voc = "aeiou"
        suma_abc = 0
        suma_voc = 0
        maximo_veces_abc = -1
        veces_abc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        veces_voc = [0, 0, 0, 0, 0]
        for i in range(len(txt)):
            for j in range(len(txt[i])):
                for k in range(len(abc)):
                    if(txt[i][j] == abc[k]):
                        veces_abc[k] += 1
                        suma_abc += 1
                for k in range(len(voc)):
                    if(txt[i][j] == voc[k]):
                        veces_voc[k] += 1
                        suma_voc += 1
        for i in range(len(veces_abc)):
            if(maximo_veces_abc < veces_abc[i]):
                maximo_veces_abc = veces_abc[i]

        porc_voc = round((suma_voc / suma_abc) * 100, 1)
        porc_con = round(100 - porc_voc, 1)
        tuple_veces_abc = []
        tuple_veces_abc.append(tuple(veces_abc))

        # Estadisticas del patron
        palabras_encontradas = []
        for i in range(len(match)):
            res = match[i]
            if res['keyword'] not in palabras_encontradas:
                palabras_encontradas.append(res['keyword'])
        patron_s = palabras_encontradas
        patron_j = "".join(palabras_encontradas)
        suma_abc_p = 0
        suma_voc_p = 0
        maximo_veces_abc_p = -1
        veces_abc_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        veces_voc_p = [0, 0, 0, 0, 0]
        for i in range(len(patron_j)):
            for k in range(len(abc)):
                if(patron_j[i] == abc[k]):
                    veces_abc_p[k] += 1
                    suma_abc_p += 1
            for k in range(len(voc)):
                if(patron_j[i] == voc[k]):
                    veces_voc_p[k] += 1
                    suma_voc_p += 1
        for i in range(len(veces_abc_p)):
            if(maximo_veces_abc_p < veces_abc_p[i]):
                maximo_veces_abc_p = veces_abc_p[i]

        porc_voc_p = round((suma_voc_p / suma_abc_p) * 100, 1)
        porc_con_p = round(100 - porc_voc_p, 1)
        tuple_veces_abc_p = []
        tuple_veces_abc_p.append(tuple(veces_abc_p))

        # Cadena de palabras unidas
        unidas = "implicito"
        unidas_t = "implicito_total"

        # Generacion de archivos output
        final = open(
            '/var/www/html/webParalela/BIBLIA/Respuestas/respuesta_' + pdf + '_' + unidas + '.json', 'w')
        texto = json.dumps(match)
        final.write(texto)

        final = open(
            '/var/www/html/webParalela/BIBLIA/Textos/' + pdf + ".txt", 'w')
        texto = json.dumps(txt)
        final.write(texto)

        # Envia email al usuario
        link = "http://00-ironman.clustermarvel.utem/webParalela/BIBLIA/index.php?pagina=" + \
            str(prim_pag_o) + "&file=" + pdf + "&pattern=" + unidas
        link = link.replace(' ', '')
        print ("\n\nAcceda (orden  ) a : ", link)

        # Preparacion de datos a enviar
        stats = {'suma_abc': suma_abc, 'suma_voc': suma_voc,
                 'porc_voc': porc_voc, 'porc_con': porc_con, 'veces_voc': veces_voc,
                 'veces_abc': veces_abc, 'tuple_veces_abc': tuple_veces_abc,
                 'maximo_veces_abc': maximo_veces_abc}

        stats_p = {'suma_abc': suma_abc_p, 'suma_voc': suma_voc_p,
                   'porc_voc': porc_voc_p, 'porc_con': porc_con_p, 'veces_voc': veces_voc_p,
                   'veces_abc': veces_abc_p, 'tuple_veces_abc': tuple_veces_abc_p,
                   'maximo_veces_abc': maximo_veces_abc_p, 'patron_corto': patron_s}

        info = {'nombre_pdf': pdf, 'patron_a_buscar': unidas_t, 'patron_corto': unidas,
                'nro_de_paginas': len(txt), 'link': link, 'salto_maximo': jumpMax}

        print(stats['veces_abc'])
        print("Paramatros Generados!")

        # Generar PDF
        # Principal(info, stats, match)
        crearPDF(pdf, keyword, "Implicita", jumpMax,
                 tiempo_final, len(match), size, stats, info, match, stats_p, documento)
        print("Documento PDF creado!")

        # Envio de Mail
        envio_mail_paralelo_implicito(
            len(match), pdf, keyword, jumpMax, email, match, len(txt), link, documento)
        print("Correo Enviado a ", email, "!\n")

        # Muestra resultados
        print("\nLa cantidad de caracteres analizados fue de: ",
              suma_abc, " con ", suma_voc, " vocales.")
        print("\nLos porcentajes encontrados fueron: ",
              porc_voc, '% vocales y ', porc_con, '% consonantes.')

run()
