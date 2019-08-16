import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import Progressbar, Notebook, OptionMenu
import easygui
import pandas as pd
from time import strftime
import datetime
import engine
import time, serialize, re

FULL_MONTHS = {1: 'Janeiro' , 2: 'Fevereiro', 3: 'Março', 4: 'Abril',  5: 'Maio',  6: 'Junho',
          7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}


window = tk.Tk() 
window.title("BudgetApp") 
window.geometry("600x200+570+150") # size of the window when it opens
#window.minsize(width=600, height=600) # you can define the minimum size of the
                          #window like this
window.resizable(width="false", height="false") # change to false if you want to prevent resizing

"""
    Tabs creation
"""
tab_parent = Notebook(window) 
tabPdf = tk.Frame(tab_parent)
tabCompare = tk.Frame(tab_parent)


"""
    Widgets (TAB1) : Frame definition and tabs
"""
frame_header = tk.Frame(tabPdf, borderwidth=0, pady=2)
center_frame = tk.Frame(tabPdf, borderwidth=2, pady=5)
bottom_frame = tk.Frame(tabPdf, borderwidth=2, pady=5)
progress_frame = tk.Frame(tabPdf, borderwidth=2, pady=5)
frame_header.grid(row=0, column=0)
center_frame.grid(row=1, column=0)
bottom_frame.grid(row=2, column=0)
progress_frame.grid(row=3, column=0)

tab_parent.add(tabPdf, text='Gerar Análise')
tab_parent.add(tabCompare, text='Comparação de gastos')

"""
    Header (TAB1)
"""
header = tk.Label(frame_header, text = "Budget APP", bg='grey', fg='black', height='3', width='43', font=("Helvetica 17 bold"))
header.grid(row=0, column=0)

"""
    Center frame division (TAB1)
    "pathDestiny" : To store the path variable defined in browseButton later
"""
### Define center frame division and create variable for path selected
frame_main_1 = tk.Frame(center_frame, borderwidth=2)
pdfPathLabel = tk.Label(frame_main_1, text = "Destino do PDF: ", font=("Helvetica 9 bold")).pack(side='left')
pathDestiny = tk.StringVar()

pathLabel = tk.Label(frame_main_1, text = '')
### Browsefile dialog
def browseButton():
    filename = filedialog.askdirectory()
    pathDestiny.set(filename)
    pathLabel.config(text = filename[:45])
    pathLabel.pack(side='left')
    return filename

### Button for calling browse dialog and packing of center frame
buttonPath = tk.Button(frame_main_1, text="Abrir", command=browseButton).pack(side='left')
frame_main_1.pack(fill='x', pady=2)

"""
    Progress frame(TAB1): contains the progress bar, the close button after PDF generation
"""
def closeWindow():
    window.destroy()

def progressBar():
    progress = Progressbar(progress_frame,orient='horizontal', length = 100, mode = 'determinate')
    progress.pack(side='left')
    progress['value'] = 20
    window.update_idletasks() 
    time.sleep(1) 
    
    progress['value'] = 45
    window.update_idletasks()  
    time.sleep(1) 
    
    progress['value'] = 60
    window.update_idletasks() 
    time.sleep(1) 
    
    progress['value'] = 80
    window.update_idletasks()
    time.sleep(1) 

    progress['value'] = 100
    progress.destroy()
    tk.Button(progress_frame, text="Fechar", command=closeWindow, bg='dark red', fg='white', relief='raised', width=20, font=('Helvetica 9 bold')).pack(side='left')

def getEmails():
    askEmails = simpledialog.askstring("Introduza email(s)","Por favor introduzir emails separados por ','", parent = window)
    listEmails = askEmails.split(",")
    return listEmails

"""
    Main workflow
"""
def run():
    window.geometry("600x240")
    if not pathDestiny.get():
        messagebox.showwarning("Informação", "Especifique o caminho de destino do PDF !")
    else:    
        result = messagebox.askquestion("E-mail","Pretende enviar email da análise ?")
        if result == 'yes':
            emails = getEmails()
            engine.run(pathDestiny.get().replace('/','\\'), True, emails)
            progressBar()
            messagebox.showinfo("E-mail enviado", "O email foi enviado")
        else: 
            engine.run(pathDestiny.get().replace('/','\\'))
            progressBar()
            messagebox.showinfo("PDF gerado", f'O PDF foi gerado para {pathDestiny.get()}')
    

"""
    Bottom frame (TAB1): generate PDF button
"""
tk.Button(bottom_frame, text=f"Gerar PDF - {FULL_MONTHS.get(engine.getMesActual())}", command=run, bg='dark green', fg='white', relief='raised', width=20, font=('Helvetica 9 bold')).pack(side='left')
tab_parent.pack(expand = 1, fill = 'both')










"""
    Tab de comparação de gastos
"""
frame_header_tab2 = tk.Frame(tabCompare, borderwidth=0, pady=2)
center_frame_tab2 = tk.Frame(tabCompare, borderwidth=2, pady=5)
bottom_frame_tab2 = tk.Frame(tabCompare, borderwidth=2, pady=5)
detailedComparsion_frame_tab2 = tk.Frame(tabCompare, borderwidth=2, pady=5)
frame_header_tab2.grid(row=0, column=0)
center_frame_tab2.grid(row=1, column=0)
bottom_frame_tab2.grid(row=2, column=0)
detailedComparsion_frame_tab2.grid(row=3, column=0)

header_tab2 = tk.Label(frame_header_tab2, text = "Comparação de gastos", bg='grey', fg='black', height='1', width='43', font=("Helvetica 17 bold"))
header_tab2.grid(row=0, column=0)

### Frame main 2 to pack label and month dropdown on the same frame
frame_main_2 = tk.Frame(center_frame_tab2, borderwidth=2)
### Bottom main 2 to pack dataframes expenses on the same frame
frame_bottom_2 = tk.Frame(bottom_frame_tab2, borderwidth=2)
### Comparsion frame to pack detailed expenses comparsion
frame_detailed_2 = tk.Frame(detailedComparsion_frame_tab2, borderwidth=2)

### DropDown menu for frame_main_2
monthVar = tk.StringVar(window)
readFiles = serialize.serialization()
menuOptions = readFiles.getFilesOnBucket('dfGastosOrdenados')

### Transforma o nome dos dataFrames em Meses
def fileToMonth(list):
    result = []
    for mes in list:
        mesAsString = re.findall(r'\d+', mes)
        month = FULL_MONTHS.get(int(mesAsString[0]))
        if month in FULL_MONTHS.values():
            result.append(month)
    return result
    
menuMonths = fileToMonth(menuOptions)
monthVar.set('Mes')

chosenMonthExpense = tk.Label(frame_bottom_2, text = '', font=("Helvetica 9 bold"))
currentMonthExpense = tk.Label(frame_bottom_2, text = '', font=("Helvetica 9 bold"))
expenseDifference = tk.Label(frame_bottom_2, text = '', font=("Helvetica 9 bold"))
def buildDisplayComparsion(dataFrame):
    chosenMonthExpense.config(text=f"{monthVar.get()} \n {dataFrame['Mes Escolhido'][0]}") 
    chosenMonthExpense.pack(side='left')
    currentMonthExpense.config(text=f"{FULL_MONTHS.get(engine.getMesActual())} \n {dataFrame['Ultimo Mes'][0]}") 
    currentMonthExpense.pack(side='left')
    
    if float(dataFrame['Mes Escolhido'][0]) > float(dataFrame['Ultimo Mes'][0]):
        diference = float(dataFrame['Mes Escolhido'][0]) - float(dataFrame['Ultimo Mes'][0])
        expenseDifference.config(fg='green')
        expenseDifference.config(text=diference) 
        expenseDifference.pack(side='left')
    else: 
        expenseDifference.config(fg='red')
        diference = round(float(dataFrame['Ultimo Mes'][0]) - float(dataFrame['Mes Escolhido'][0]), 2)
        expenseDifference.config(text=f"Diferença: \n {diference} Euros") 
        expenseDifference.pack(side='left')

supermercadoChosen = tk.Label(frame_detailed_2, text = '', font=("Helvetica 9 bold"))
supermercadoCurrent = tk.Label(frame_detailed_2, text = '', font=("Helvetica 9 bold"))
expenseSupermerketDifference = tk.Label(frame_detailed_2, text = '', font=("Helvetica 9 bold"))
def buildDisplayComparsionDetailed(dfMesAnterior, dfMesActual):
    valorSupermercadoPassado = dfMesAnterior.loc[dfMesAnterior['Entidade']=='SUPERMERCADOS', ['Valor']].values[0][0]
    valorSupermercadoCurrente = dfMesActual.loc[dfMesActual['Entidade']=='SUPERMERCADOS', ['Valor']].values[0][0]
    supermercadoChosen.config(text=f"Supermercados em {monthVar.get()} \n {valorSupermercadoPassado}") 
    supermercadoChosen.pack(side='left')
    supermercadoCurrent.config(text=f"Supermercados em {FULL_MONTHS.get(engine.getMesActual())} \n {valorSupermercadoCurrente}") 
    supermercadoCurrent.pack(side='left')
    
    if float(valorSupermercadoPassado) > float(valorSupermercadoCurrente):
        diference = valorSupermercadoPassado - valorSupermercadoCurrente
        expenseSupermerketDifference.config(fg='green')
        expenseSupermerketDifference.config(text=f"Diferença: \n {diference} Euros") 
        expenseSupermerketDifference.pack(side='left')
    else:
        diference = valorSupermercadoCurrente - valorSupermercadoPassado
        expenseSupermerketDifference.config(fg='red')
        expenseSupermerketDifference.config(text=f"Diferença: \n {diference} Euros")
        expenseSupermerketDifference.pack(side='left')
    

def compareExpenses():
    window.geometry("600x540")
    mes = str(monthVar.get())
    fileToDownload = [k for k,v in FULL_MONTHS.items() if v == mes]
    nameOfFile = f"dfGastosOrdenados{str(fileToDownload[0])}"
    dfMesAnterior = readFiles.fileToDfDownload(nameOfFile)
    dfMesActual = readFiles.fileToDfDownload(f"dfGastosOrdenados{str(engine.getMesActual())}")
    dfComparsion = engine.compareMonths(dfMesAnterior, dfMesActual)
    buildDisplayComparsion(dfComparsion)
    buildDisplayComparsionDetailed(dfMesAnterior, dfMesActual)

 
    

### Label and dropdown menu packed on the same frame
optionMonth = OptionMenu(frame_main_2, monthVar, 'Seleccione o mês',  *menuMonths).pack(side='left') 
tk.Button(frame_main_2, text="OK", command=compareExpenses, bg='dark green', fg='white', relief='raised', width=10, font=('Helvetica 7 bold')).pack(side='left')

frame_main_2.pack(fill='x', pady=2)
frame_bottom_2.pack(fill='x', pady=2)
frame_detailed_2.pack(fill='x', pady=2)



"""
    MainLoop
"""
window.mainloop()

# TODO: list of emails editable (dialog for entering)
# TODO : Fix progressbar stalling

"""
    V2.0:
        Serialization : Now we are able to compare total expense from previous months
        Tabs: New tab for budget comparsion
        ProgressBar: progress bar to controll PDF generation status
"""


