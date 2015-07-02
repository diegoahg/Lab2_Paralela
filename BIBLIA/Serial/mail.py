import requests


def envio_mail_serial_implicito(largo, pdf, keyword, jumpMax, email, match, n_pages, link):
    name = ["Resumen", pdf, "Implicita", str(jumpMax)]
    nombre_pdf = "_".join(name)
    palabras_encontradas = []
    palabras_unicas = []
    cont = 0
    palabras_temp = []

    for i in range(len(match)):
        res = match[i]
        if res['keyword'] not in palabras_unicas:
            palabras_temp.append(res['keyword'])
            palabras_unicas.append(res['keyword'])
            cont += 1
        if cont == 5:
            palabras_encontradas.append(" ".join(palabras_temp))
            palabras_temp = []
            cont = 0

    if len(match) > 0:
        return requests.post(
            "https://api.mailgun.net/v3/sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org/messages",
            auth=("api", "key-bccd075f02a12db1dee03a7710800a5d"),
            files=[
                ("attachment", open("/var/www/html/webParalela/BIBLIA/PDF/" + nombre_pdf + ".pdf", encoding='ISO-8859-1'))],
            data={"from": "Cluster Marvel<postmaster@sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org>",
                  "to": "Usuario <" + email + ">",
                  "subject": "Resultados Bible Code - SERIAL IMPLICITO",
                  "text":
                  "Busqueda en <" + pdf.upper() +
                  ".pdf> terminada.\n" +
                  "____________________________________________\n\n" + "En la busqueda se encontro " + str(len(palabras_unicas)) +
                  " resultados, los que se listan a continuacion:\n -> " + "\n -> ".join(palabras_encontradas) +
                  "\n____________________________________________" +
                  "\n\nSe encontraron: " + str(largo) + " resultados con un salto maximo de " + str(jumpMax) + " posiciones en las " +
                  str(n_pages) + " paginas del documento." +
                  "\n\nPara ver el detalle, ingrese a: " + link})
    else:
        return requests.post(
            "https://api.mailgun.net/v3/sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org/messages",
            auth=("api", "key-bccd075f02a12db1dee03a7710800a5d"),
            data={"from": "Cluster Marvel<postmaster@sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org>",
                  "to": "Usuario <" + email + ">",
                  "subject": "Resultados Bible Code - SERIAL IMPLICITO",
                  "text":
                  "Busqueda en <" + pdf.upper() +
                  ".pdf> terminada.\n" +
                  "____________________________________________\n\n" +
                  "En la busqueda NO se encontraron resultados. Intente con nuevos parametros" +
                  "\n____________________________________________" +
                  "\n\nSe buscaron resultados con un salto maximo de " + str(jumpMax) + " posiciones en las " +
                  str(n_pages) + " paginas del documento."})


def envio_mail_serial_explicito(largo, pdf, keyword, jumpMax, email, match, patron_corto, n_pages, link):
    words = "_".join(keyword)
    name = ["Resumen", pdf, words, str(jumpMax)]
    nombre_pdf = "_".join(name)
    print("Documento: PDF/" + nombre_pdf + ".pdf enviado a: " + email)

    if len(match) > 0:
        return requests.post(
            "https://api.mailgun.net/v3/sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org/messages",
            auth=("api", "key-bccd075f02a12db1dee03a7710800a5d"),
            files=[
                ("attachment", open("/var/www/html/webParalela/BIBLIA/PDF/" + nombre_pdf + ".pdf", encoding='ISO-8859-1'))],
            data={"from": "Cluster Marvel<postmaster@sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org>",
                  "to": "Usuario <" + email + ">",
                  "subject": "Resultados Bible Code - SERIAL EXPLICITO",
                  "text":
                  "Busqueda en <" + pdf.upper() + ".pdf> terminada.\n" +
                  "____________________________________________\n\n" +
                  "En la busqueda consistio en buscar las " + str(len(patron_corto.split("_"))) + " palabras que se listan a continuacion:\n -> " +
                  "\n -> ".join(patron_corto.split("_")) + "\n____________________________________________" +
                  "\n\nSe encontraron: " + str(largo) + " resultados con un salto maximo de " + str(jumpMax) +
                  " posiciones en las " + str(n_pages) + " paginas del documento." +
                  "\n\nPara ver el detalle, ingrese a: " + link})
    else:
        return requests.post(
            "https://api.mailgun.net/v3/sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org/messages",
            auth=("api", "key-bccd075f02a12db1dee03a7710800a5d"),
            data={"from": "Cluster Marvel<postmaster@sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org>",
                  "to": "Usuario <" + email + ">",
                  "subject": "Resultados Bible Code - SERIAL EXPLICITO",
                  "text":
                  "Busqueda en <" + pdf.upper() +
                  ".pdf> terminada.\n" +
                  "____________________________________________\n\n" +
                  "En la busqueda NO se encontraron resultados. Intente con nuevos parametros" +
                  "\n____________________________________________" +
                  "\n\nSe buscaron resultados con un salto maximo de " + str(jumpMax) + " posiciones en las " +
                  str(n_pages) + " paginas del documento."})
