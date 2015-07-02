import requests

def envio_mail(mail, nombre):
  return requests.post(
      "https://api.mailgun.net/v3/sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org/messages",
      auth=("api", "key-bccd075f02a12db1dee03a7710800a5d"),
      files=[("attachment", open("/var/www/html/webParalela/PERCOLACION/"+nombre+".pdf"))],
      data={"from": "Cluster Marvel<postmaster@sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org>",
            "to": "<"+mail+">",
            "subject": "Resultados propagacion de incendios forestales",
            "text":
            "\nMuchas gracias por utilizar nuestra plataforma para resolver sus requerimientos."
            "\n\n"
            "Se adjunta como respuesta un PDF con los resultados ("+nombre+".pdf)."
            "\n\nRealizado por: http://00-ironman.clustermarvel.utem/webParalela/"})