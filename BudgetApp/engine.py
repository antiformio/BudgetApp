
import pygsheets, smtplib
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt #pip install matplotlib
import numpy as np #pip install numpy
from matplotlib.backends.backend_pdf import PdfPages
import six #pip install six
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

supermercados = ['BON AREA', 'MERCADONA', 'DIA', 'VUIT SANT PERE', 'LA NUPA', 'LIDL','SUPERMERCAT']
renda = 'TEFASA GRUP IMMOBILIARI'
telemoveis = ['ORANGE', 'CARD RECHARGING']
ginasios = ['GCD-BARCELONA', 'MCFIT', 'LEISURE ORGANIZATION', 'GESTORA CLUBS DIR' ]
internet = ['PEPEPHONE']
electricidade = 'ENDESA'


def auth():
    return pygsheets.authorize(service_file='BudgetLogin.json')

def openBook(gc,title):
    return gc.open(title)

def getSheet(book, name):
    return book.worksheet_by_title(name)

def getMesActual():
    return datetime.now().month - 1

def getRawDataByAccount(gc, tipo):
        book = openBook(gc, tipo + str(getMesActual()))
        sheet = getSheet(book, "Sheet1")
        return sheet.get_all_values()

def populateDic(rawList):
    dicOutgoing = {}
    dicIncoming = {}
    for entry in rawList:
        if entry[1] != '' and float(entry[3].replace(',','.')) < 0:
            if entry[1] not in dicOutgoing.keys():
                dicOutgoing[entry[1]] = abs(float(entry[3].replace(',','.')))
            else:
                dicOutgoing[entry[1]] = dicOutgoing.get(entry[1]) + abs(float(entry[3].replace(',','.')))
        elif entry[1] != '' and float(entry[3].replace(',','.')) > 0:
            if entry[1] not in dicIncoming.keys():
                dicIncoming[entry[1]] = float(entry[3].replace(',','.'))
            else:
                dicIncoming[entry[1]] = dicIncoming.get(entry[1]) + float(entry[3].replace(',','.'))
    return dicOutgoing, dicIncoming

def cleanEntry(rawList):
    for entry in rawList:
        if entry[1] != '' and entry[1][0:8] == 'PURCHASE':
            entry[1] = entry[1][36:]
            if any(x in entry[1] for x in supermercados):
                entry[1] = 'SUPERMERCADOS'
            elif any(x in entry[1] for x in telemoveis):
                entry[1] = 'CARREGAMENTOS TELEMOVEIS'
            #Retirar se ficar pouco detalhado
            # else:
            #     entry[1] = 'OUTROS GASTOS'

        elif entry[1] != '' and entry[1][0:10] == 'WITHDRAWAL':
            entry[1] = 'LEVANTAMENTOS'

        elif entry[1] != '' and renda in entry[1]:
            entry[1] = 'RENDA'

        elif any(x in entry[1] for x in telemoveis):
            entry[1] = 'CARREGAMENTOS TELEMOVEIS'

        elif entry[1] != '' and entry[1][0:13] == 'PAYMENT BIZUM':
            entry[1] = 'BIZUM'

        elif any(x in entry[1] for x in ginasios):
            entry[1] = 'GINÁSIOS'

        elif any(x in entry[1] for x in internet):
            entry[1] = 'INTERNET'

        elif any(x in entry[1] for x in electricidade):
            entry[1] = 'ELECTRICIDADE'
        #Retirar se ficar pouco detalhado...
        # elif entry[1] != '':
        #     entry[1] = 'OUTROS GASTOS'
    return rawList



def graficoPieNovo(df):
    fig = plt.figure()

    patches, texts = plt.pie(df["Valor"],
            startangle = 90, radius=1.3
            )

    labels = [x[0:19] for x in df["Entidade"]]
    plt.legend(patches, labels, bbox_to_anchor=(-0.7, 1.),
               fontsize=6)
    plt.tight_layout()
    fig.suptitle('Distribuição de gastos', size=19)
    #plt.show()

    return fig

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=12,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)


    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

def sendEMail(filename, tipo):
    destino = ['fjnmgm@gmail.com']
    mail = MIMEMultipart()
    mail['From'] = 'aws.py.servidor@gmail.com'
    mail['To'] = ", ".join(destino)
    mail['Cc'] = ''
    mail['Subject'] = tipo+ ' do mês de ' +str(getMesActual())
    text = ""

    fo = open(filename, 'rb')
    attach = MIMEApplication(fo.read(), _subtype="pdf")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)
    mail.attach(attach)

    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login('aws.py.servidor@gmail.com', 'ketooketyr')
    conn.sendmail(mail['From'], destino, mail.as_string())
    conn.quit()

def run(path, email=None):
    gc = auth()

    """
        'comum' - Para a conta comum 
        'minha' - Para a minha conta
    """
    dataClean = cleanEntry(getRawDataByAccount(gc, 'comum'))

    """
        Dictionaries
    """
    dicGastos, dicIncome = populateDic(dataClean)

    for valor in dicGastos:
        for k, v in dicGastos.items():
            dicGastos[k] = round(v, 2)

    """
        Dataframes
    """
    dfGastos = pd.DataFrame(dicGastos.items(), columns=["Entidade", "Valor"])
    #dfIncome = pd.DataFrame(dicIncome.items(), columns=["Entidade", "Valor"])

    """
        
        Gráfico 
        
    """
    nomeFile = f'AnáliseGastos{getMesActual()}.pdf'
    os.chdir(path)
    pp = PdfPages(nomeFile)

    plotPieGastos = graficoPieNovo(dfGastos)
    pp.savefig(plotPieGastos)

    """
        
        Dataframes to PDF
        
    """
    df4maisCaros = dfGastos.nlargest(4, columns=["Valor"])
    dfGastosOrdenados = dfGastos.sort_values('Valor', ascending=False)
    dfGastosTotal = round(dfGastos['Valor'].sum(),2)

    axMaisCaros = render_mpl_table(df4maisCaros, header_columns=0, col_width=6.0)
    figMaisCaros = axMaisCaros.get_figure()
    figMaisCaros.suptitle('Top do mês', fontsize=19)
    pp.savefig(figMaisCaros)

    axOrdenado = render_mpl_table(dfGastosOrdenados, header_columns=0, col_width=6.0)
    figOrdenado = axOrdenado.get_figure()
    figOrdenado.suptitle('Gastos por ordem', fontsize=19)
    pp.savefig(figOrdenado)

    fig = plt.figure()
    fig.suptitle('Gastos totais do mes', fontsize=19)
    fig.text(0.5,0.8, f'{dfGastosTotal} Euros', fontsize = 12)
    pp.savefig(fig)

    pp.close()

    filename = path + '\\' + 'AnáliseGastos' + str(getMesActual())+'.pdf'
    # Ultimo parametro pode ser Gastos ou Income
    if email:
        sendEMail(filename, 'Gastos')
