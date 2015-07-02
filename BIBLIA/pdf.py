from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time
import math

# parametros a utilizar en la creacion del pdf


def crearPDF(pdf, keyword, forma, salto, tiempo, n_match, np, stats, info, match, stats_p, documento):
    words = ""
    if(forma == "Implicita"):
        name = ["Resumen", pdf, "Implicita", str(salto)]
    else:
        words = "_".join(keyword)
        name = ["Resumen", pdf, words, str(salto)]

    nombre_pdf = "_".join(name)
    c = canvas.Canvas(
        "/var/www/html/webParalela/BIBLIA/PDF/" + documento + ".pdf", pagesize=letter)
    # cabecera
    c.setFont("Helvetica-Oblique", 10)
    c.drawImage("logo.png", 10, 690, width=90, height=90)
    c.drawString(110, 765, "Universidad Tecnologica Metropolitana de Chile")
    c.drawString(
        110, 753, "Ingenieria Civil en Computacion Mencion Informatica")
    c.drawString(110, 741, "Computacion Paralela")
    c.drawString(110, 729, "Plataforma Integrada")

    # Titulo
    c.setFont("Helvetica-Bold", 30)
    c.drawString(180, 629, "Resultado Biblia")
    c.line(50, 620, 562, 620)
    # Subtitulo
    c.setFont("Helvetica-Oblique", 20)
    c.drawString(220, 600, "Busqueda " + forma)

    # SUBTITULO 2
    if(forma == "Implicita"):
        patron = "mediante busqueda implicita."
    else:
        patron = " ".join(stats_p['patron_corto'])
    sPatron = "Patron : " + patron
    c.setFont("Helvetica-Bold", 17)
    c.drawString(50, 550, sPatron)

    # Cuerpo
    # input
    c.setFont("Helvetica", 15)
    c.drawString(
        50, 530, "A continuacion se muestran los datos solicitados, las coincidencias y estadisti-")
    c.drawString(
        50, 512, "cas del proceso de investigacion solicitado en la plataforma web. ")
    c.setFont("Helvetica-Oblique", 14)
    sDocumento = "Documento: " + pdf + ".pdf"
    sSalto = "Salto Maximo: " + str(salto) + " posiciones."
    sNP = "Nro de Procesadores: " + str(np) + " en total."
    sTotal = "Total de Coincidencias: " + str(n_match) + " veces."
    sTiempo = "Tiempo de ejecucion: " + str(round(tiempo, 1)) + " segundos."
    sPaginas = "Nro de Paginas: " + str(info['nro_de_paginas']) + "."
    c.drawString(50, 460, sDocumento)
    c.drawString(50, 480, sSalto)
    c.drawString(50, 440, sNP)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(306, 440, sPaginas)
    c.drawString(306, 460, sTotal)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(306, 480, sTiempo)

    # output

    # Subtitulo
    c.setFont("Helvetica-Bold", 20)
    c.drawString(130, 380, "Estadisticas del Documento")
    c.setFont("Helvetica", 15)

    # info 0-> nombre_pdf 1->patron_a_buscar 2->nro_de_paginas 3-> link 4-> salto_maximo
    # stats {'suma_abc','suma_voc','porc_voc','porc_con','veces_voc','veces_abc','tuple_veces_abc','maximo_veces_abc'}
    # stats_p {'suma_abc','suma_voc','porc_voc','porc_con','veces_voc','veces_abc','tuple_veces_abc','maximo_veces_abc'}
    # match {<coincidencias>}

    c.setFont("Helvetica", 15)
    c.drawString(
        50, 350, "El analisis del texto del pdf arrojó los siguientes resultados: ")
    CC = "- Cantidad de caracteres analizados: " + \
        str(stats['suma_abc']) + " letras en el texto."
    SV = "- Total de Vocales: " + str(stats['suma_voc']) + " en el texto."
    PV = "- Porcentaje de Vocales: " + str(stats['porc_voc']) + "% del total ."
    PC = "- Porcentaje de Consonantes: " + \
        str(stats['porc_con']) + "% del total ."
    c.setFont("Helvetica", 15)
    c.drawString(70, 330, CC)
    c.drawString(70, 310, SV)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(70, 290, PV)
    c.drawString(70, 270, PC)

    # Subtitulo 2
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 230, "Estadisticas del Patron Alfabetico")
    c.setFont("Helvetica", 15)

    c.setFont("Helvetica", 15)
    c.drawString(
        50, 200, "El analisis del patron de busqueda, arrojó los siguientes resultados: ")
    CC = "- El patron posee " + \
        str(stats_p['suma_abc']) + " caracteres en total."
    SV = "- Total de Vocales: " + str(stats_p['suma_voc']) + "."
    TP = "- Cantidad de Palabras: " + str(len(stats_p['patron_corto'])) + "."
    PV = "- Porcentaje de Vocales: " + \
        str(stats_p['porc_voc']) + "% del total ."
    PC = "- Porcentaje de Consonantes: " + \
        str(stats_p['porc_con']) + "% del total ."
    c.setFont("Helvetica", 15)
    c.drawString(70, 180, CC)
    c.drawString(70, 160, SV)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(70, 140, PV)
    c.drawString(70, 120, PC)
    c.drawString(370, 180, TP)

    c.setFont("Helvetica", 15)
    c.drawString(
        50, 60, "Para ver los resultados en detalle y de forma grafica, visite el siguiente link: ")
    c.setFont("Courier-Oblique", 8)
    c.drawString(50, 45, info['link'])

    # Pie de pagina
    c.line(20, 40, 582, 40)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(
        140, 30, "Recuerda seguir utilizando nuestra pagina : 00-ironman.clustermaarvel.utem/webParalela/biblia.php")
    now = "Documento creado en :" + time.strftime("%c")
    c.drawString(230, 20, now)
    c.showPage()

    # info 0-> nombre_pdf 1->patron_a_buscar 2->nro_de_paginas 3-> link 4-> salto_maximo
    # stats {'suma_abc','suma_voc','porc_voc','porc_con','veces_voc','veces_abc','tuple_veces_abc','maximo_veces_abc'}
    # stats_p {'suma_abc','suma_voc','porc_voc','porc_con','veces_voc','veces_abc','tuple_veces_abc','maximo_veces_abc'}
    # match {<coincidencias>}
    
    resumen = []
    n_pres = 0
    for i in range( info['nro_de_paginas'] ):
        con_pag = {'pagina': 0, 'palabras': []}
        cont = 0
        for j in range(len(match)):
            if match[j]['pagina'] == (i+1) and match[j]['keyword'] not in con_pag['palabras'] and cont <= 10:
                con_pag['palabras'].append(match[j]['keyword'])
                if cont ==10 :
                    con_pag['palabras'].append("[ + mas]")
                cont += 1
        con_pag['pagina'] = i+1
        resumen.append(con_pag)
    
    for i in range(len(resumen)):
        if len(resumen[i]['palabras']) > 0 :
            n_pres += 1
    
    faltan = 1
    primero = 0
    
    for i in range( math.ceil( n_pres/21 ) ) :
    # while(faltan==1):        
        # cabecera pagina 2
        c.setFont("Helvetica-Oblique", 10)
        c.drawImage("logo.png", 10, 690, width=90, height=90)
        c.drawString(110, 765, "Universidad Tecnologica Metropolitana de Chile")
        c.drawString(110, 753, "Ingenieria Civil en Computacion Mencion Informatica")
        c.drawString(110, 741, "Computacion Paralela")
        c.drawString(110, 729, "Plataforma Integrada")
        
        # Subtitulo PAGINA 2
        c.setFont("Helvetica-Bold", 20)
        c.drawString(170, 690, "Detalle de Resultados")
        
        # Pie de pagina 2
        c.line(20, 40, 582, 40)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(140, 30, "Recuerda seguir utilizando nuestra pagina : 00-ironman.clustermaarvel.utem/webParalela/biblia.php")
        now = "Documento creado en :" + time.strftime("%c")
        c.drawString(230, 20, now)
        pos_x = 660
        cont = 0
        
        for i in range(primero, len(resumen)) :
            if len(resumen[i]['palabras']) > 0 :
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, pos_x, "Palabras encontradas en pagina " + str(i+1) + " :")
                c.setFont("Helvetica-Oblique", 12)
                p = resumen[i]['palabras']
                c.drawString(50, pos_x - 15, " ".join(p))
                cont += 1
                pos_x -= 30
            if cont > 20 :
                primero = i+1 
                break
        
        c.showPage()

    c.save()

    print("EXITO PDF!")
