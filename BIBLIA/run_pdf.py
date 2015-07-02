#!/usr/bin/env python

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1]
styles = getSampleStyleSheet()
Title = "Resultados CODE BIBLE 2015"
Author = "Brian K. Jones"
URL = "http://www.protocolostomy22.com"
email = "miguel.nunez@ceinf.cl"
Abstract = """Miguel Angel"""
Elements = []
HeaderStyle = styles["Heading1"]
ParaStyle = styles["Normal"]
PreStyle = styles["Code"]


def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
    s = Spacer(0.2 * inch, sep * inch)
    para = klass(txt, style)
    sect = [s, para]
    result = KeepTogether(sect)
    return result


def letrasGrafico(data):
    "Make a slightly pathologic bar chart with only TWO data items."
    drawing = Drawing(800, 300)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = -10
    bc.height = 300
    bc.width = 300
    bc.barWidth = 15
    bc.Title = "Frencuencias en "
    bc.data = data
    #bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 7000
    bc.valueAxis.valueStep = 500
    bc.categoryAxis.labels.boxAnchor = 'e'
    bc.categoryAxis.labels.angle = 0
    abc = "abcdefghijklmnopqrstuvwxyz"
    bc.categoryAxis.categoryNames = list(abc)
    drawing.add(bc)
    return drawing


def p(txt):
    return header(txt, style=ParaStyle, sep=0.1)


def pre(txt):
    s = Spacer(0.1 * inch, 0.1 * inch)
    p = Preformatted(txt, PreStyle)
    precomps = [s, p]
    result = KeepTogether(precomps)
    return result


def go():
    doc = SimpleDocTemplate('prueba_pdf_biblia.pdf')
    doc.build(Elements)


def Principal(info, stats, match):
    # info 0-> nombre_pdf 1->patron_a_buscar 2->nro_de_paginas 3-> link 4-> salto_maximo
    # stats {'suma_abc','suma_voc','porc_voc','porc_con','veces_voc','veces_abc','tuple_veces_abc','maximo_veces_abc'}
    # match {<coincidencias>}

    print (stats['veces_abc'])

    # Creacion e Insercion del TITULO
    mytitle = header(Title)
    myname = header(Author, sep=0.1, style=ParaStyle)
    mysite = header(URL, sep=0.1, style=ParaStyle)
    mymail = header(email, sep=0.1, style=ParaStyle)

    # Creacion e Insercion del ABSTRACT
    abstract_title = header("ABSTRACT")
    myabstract = p(Abstract)
    head_info = [mytitle, myname, mysite, mymail, abstract_title, myabstract]
    Elements.append(head_info)

    # Creacion e Insercion del CONTENIDO
    code_title = header("Basic code to produce output")
    code_explain = p("""This is a snippet of code. It's an example using the Preformatted flowable object, which
                     makes it easy to put code into your documents. Enjoy!""")
    code_source = pre("""     """)
    codesection = [code_title, code_explain, code_source]
    src = KeepTogether(codesection)
    Elements.extend(src)

    # Creacion e Insercion del CONTENIDO
    code_title = header("Basic code to produce output")
    code_explain = p("""This is a snippet of code. It's an example using the Preformatted flowable object, which
                     makes it easy to put code into your documents. Enjoy!""")
    code_source = pre("""
    def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
        s = Spacer(0.2*inch, sep*inch)
        para = klass(txt, style)
        sect = [s, para]
        result = KeepTogether(sect)
        return result
     
    def p(txt):
        return header(txt, style=ParaStyle, sep=0.1)
     
    def pre(txt):
        s = Spacer(0.1*inch, 0.1*inch)
        p = Preformatted(txt, PreStyle)
        precomps = [s,p]
        result = KeepTogether(precomps)
        return result
     
    def go():
        doc = SimpleDocTemplate('gfe.pdf')
        doc.build(Elements)
        """)
    codesection = [code_title, code_explain, code_source]
    src = KeepTogether(codesection)
    Elements.extend(src)

    # Creacion e Insercion del GRAFICO
    hourly_title = header("Frecuencia de cada Letra en el PDF")
    hourly_explain = p(
        """El siguiente grafico muestra la distribucion de las letras del abecedario dentro del documento pdf.
        Este analisis constituye la representacion formal de la frecuencia de cada letra en todas las paginas del archivo que fue analizado. 
        Se utilizara con fines estadisticos y ejemplificadores. """)
    hourly_chart = letrasGrafico(stats['tuple_veces_abc'])
    hourly_section = [hourly_title, hourly_explain, hourly_chart]
    Elements.extend(hourly_section)

    go()
