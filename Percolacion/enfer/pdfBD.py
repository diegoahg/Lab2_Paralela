from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time

# parametros a utilizar en la creacion del pdf


def crearPDFBD(enfe, dist, tam, mean, tiempo, nombre):

    # Agregar los mensajes de probabilidades en cada caso

    if enfe == 1:
        nomenfe = "Gripe"
        mensaje = "Por sus caracteristicas, "
        if 0 < mean < 0.5:
            mensaje1 = "no necesita mayor cuidado por tener un contagio bajo."
        if 0.5 < mean < 0.75:
            mensaje1 = "se recomienda el aumento en la medicina."
        if 0.75 < mean:
            mensaje1 = "se recomienda preparar los servicios de atencion."
    if enfe == 2:
        nomenfe = "Sarampion"
        mensaje = "Por sus caracteristicas, "
        if 0 < mean < 0.6:
            mensaje1 = "no necesita mayor cuidado por tener un contagio bajo."
        if 0.6 < mean < 0.8:
            mensaje1 = "se recomienda el aumento en la medicina."
        if 0.8 < mean:
            mensaje1 = "se recomienda preparar los servicios de atencion."
    if enfe == 3:
        nomenfe = "Meningitis"
        mensaje = "Por sus caracteristicas, "
        if 0 < mean < 0.3:
            mensaje1 = "no necesita mayor cuidado por tener un contagio bajo."
        if 0.3 < mean < 0.6:
            mensaje1 = "se recomienda el aumento en la medicina."
        if 0.6 < mean:
            mensaje1 = "se recomienda preparar los servicios de atencion."
    if enfe == 4:
        nomenfe = "Pediculosis"
        mensaje = "Por sus caracteristicas, "
        if 0 < mean < 0.5:
            mensaje1 = "no necesita mayor cuidado por tener un contagio bajo."
        if 0.5 < mean < 0.75:
            mensaje1 = "se recomienda el aumento en la medicina."
        if 0.75 < mean:
            mensaje1 = "se recomienda preparar los servicios de atencion."
    if enfe == 5:
        nomenfe = "Paperas"
        mensaje = "Por sus caracteristicas, "
        if 0 < mean < 0.6:
            mensaje1 = "no necesita mayor cuidado por tener un contagio bajo."
        if 0.6 < mean < 0.85:
            mensaje1 = "se recomienda el aumento en la medicina."
        if 0.85 < mean:
            mensaje1 = "se recomienda preparar los servicios de atencion."
    if enfe == 6:
        nomenfe = "AN1H1"
        mensaje = "Por sus caracteristicas, "
        if 0 < mean < 0.3:
            mensaje1 = "no necesita mayor cuidado por tener un contagio bajo."
        if 0.3 < mean < 0.5:
            mensaje1 = "se recomienda el aumento en la medicina."
        if 0.5 < mean:
            mensaje1 = "se recomienda preparar los servicios de atencion."

    #ancho = 612
    #alto = 792
    name = "/var/www/html/webParalela/PERCOLACION/" + nombre + ".pdf"
    c = canvas.Canvas(name, pagesize=letter)

    # cabecera
    c.setFont("Helvetica-Oblique", 8)
    c.drawImage(
        "/mpi/Percolacion/perFinal/logo.png", 10, 700, width=50, height=50)
    c.drawString(70, 740, "Universidad Tecnologica Metropolitana de Chile")
    c.drawString(
        70, 730, "Ingenieria Civil en Compiutacion Mencion Informtica")
    c.drawString(70, 720, "Computacion Paralela")
    c.drawString(70, 710, "Plataforma Integrada")

    # Titulo
    c.setFont("Helvetica-Bold", 30)
    c.drawString(140, 629, "Resultado Percolacion")
    c.line(50, 620, 562, 620)
    # Subtitulo
    c.setFont("Helvetica-Oblique", 20)
    c.drawString(200, 600, "Propagacion enfermedades")

    # Cuerpo
    # input
    c.setFont("Helvetica", 15)
    c.drawString(
        100, 550, "Los parametros de entrada para esta simulacion son:")
    c.setFont("Helvetica-Oblique", 15)
    senfe = "Enfermedad: " + nomenfe
    sDist = "Distribucion: " + str(dist) + "%"
    sTam = "Tamano: " + str(tam) + " Personas"

    c.drawString(150, 500, senfe)
    c.drawString(150, 480, sDist)
    c.drawString(306, 480, sTam)
    # output
    c.setFont("Helvetica", 15)
    c.drawString(
        100, 415, "Luego de haber realizado 385 repeticiones para obtener un")
    c.drawString(
        100, 398, "error menor al 5% podemos obtener los siguientes resultados: ")
    sMean = "Probabilidad de propagacion de la enfermedad: " + str(mean)
    meanpor = round(mean, 3) * 100
    sMeanPor = "Equivalente a un: " + str(meanpor) + "%."
    sTiempo = "Tiempo de ejecucion de la simulacion: " + \
        str(tiempo) + " Segundos"
    c.drawString(150, 348, sMean)
    c.drawString(150, 328, sMeanPor)
    c.drawString(150, 308, sTiempo)
    c.drawString(150, 260, mensaje)
    c.drawString(150, 240, mensaje1)

    # Pie de pagina
    c.line(20, 40, 582, 40)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(
        180, 30, "Recuerda seguir utilizando nuestra pagina : 00-ironman.clustermaarvel.utem")
    now = "Documento creado en :" + time.strftime("%c")
    c.drawString(230, 20, now)
    c.showPage()
    c.save()
