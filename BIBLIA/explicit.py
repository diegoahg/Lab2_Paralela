from Serial.formatPDF import toStringFormat
from Serial.searchMatches import buscaPatron
from Serial.mail import envio_mail_serial_explicito
from time import *
import sys
import json
from run_pdf import Principal
from pdf import crearPDF

# Se lee el argumento 2 con el nombre del documento pdf
pdf = str(sys.argv[1])
direccion = "Serial/" + pdf + ".pdf"

# Transforma el texto del pdf en texto, y se almacena en la variable txt.
txt = toStringFormat(direccion)

# Recibe patron por consola
keyword = str(sys.argv[2])
keyword = keyword.split()

# Recibe Salto Maximo y Correo por consola
jumpMax = int(sys.argv[3])
email = str(sys.argv[4])

# Invierte la palabra ingresada
keyword = keyword + [w[::-1] for w in keyword]

# Almaceno los resultados en una sola variable
match = []

# Comienza la medicion de tiempos
start = time()

# Etapa Principal en que se buscan Resultados
for i in range(len(keyword)):
    match += buscaPatron(txt, keyword[i], jumpMax)

# Muestra Resultados
if (len(match) == 0):
    print("Recopilacion Nodo Maestro 00-Ironman (Secuencial)")
    print(
        "*******************************************************************************\n")
    print("\tResultado Final : NO SE ENCONTRO LA PALABRA")
else:
    print("")
    print("Recopilacion Nodo Maestro 00-Ironman (Secuencial)")
    print(
        "\n*****************************************************************************\n")
    for i in range(len(match)):
        print(match[i])
    print(
        "\n*****************************************************************************\n")
    print("\tResultado Final : ", len(match), ".")
    print(
        "\n*****************************************************************************\n")
    tiempo_final = round(time() - start, 3)
    print("\tTiempo estimado de ejecucion: ", tiempo_final,
          " segundos. En recorrer ", len(txt), " paginas. Salto Maximo: ", jumpMax, ".")
    print(
        "\n*****************************************************************************\n")

    prim_pag_o = 1  # json.loads('["dato":'+match[0]+']')

    # Estadisticas del pdf
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
    patron_s = str(sys.argv[2]).split()
    patron_j = str(sys.argv[2]).replace(' ', '')
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
    unidas = "_".join(str(sys.argv[2]).split())
    unidas_t = "_".join(str(keyword))

    # Generacion de archivos output
    final = open(
        '/var/www/html/webParalela/BIBLIA/Respuestas/respuesta_' + pdf + '_' + unidas + '.json', 'w')
    texto = json.dumps(match)
    final.write(texto)

    final = open('/var/www/html/webParalela/BIBLIA/Textos/' + pdf + ".txt", 'w')
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
    crearPDF(pdf, keyword, "Explicita", jumpMax,
             tiempo_final, len(match), 1, stats, info, match, stats_p)
    print("Documento PDF creado!")

    # Envio de Mail
    envio_mail_serial_explicito(
        len(match), pdf, keyword, jumpMax, email, match, info['patron_corto'], len(txt), link)
    print("Correo Enviado a ", email, "!\n")

    # Muestra resultados
    print("\nLa cantidad de caracteres analizados fue de: ",
          suma_abc, " con ", suma_voc, " vocales.")
    print("\nLos porcentajes encontrados fueron: ",
          porc_voc, '% vocales y ', porc_con, '% consonantes.')
