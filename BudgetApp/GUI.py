
import tkinter as tk
from tkinter import filedialog, messagebox
import easygui
import pandas as pd
from time import strftime
import engine


window = tk.Tk() 

window.title("BudgetApp") 
window.geometry("600x250") # size of the window when it opens
#window.minsize(width=600, height=600) # you can define the minimum size of the
                          #window like this
window.resizable(width="false", height="false") # change to false if you want to prevent resizing


# WIDGETS
frame_header = tk.Frame(window, borderwidth=0, pady=2)
center_frame = tk.Frame(window, borderwidth=2, pady=5)
bottom_frame = tk.Frame(window, borderwidth=2, pady=5)
frame_header.grid(row=0, column=0)
center_frame.grid(row=1, column=0)
bottom_frame.grid(row=2, column=0)

header = tk.Label(frame_header, text = "Budget APP", bg='grey', fg='black', height='3', width='43', font=("Helvetica 17 bold"))
header.grid(row=0, column=0)

frame_main_1 = tk.Frame(center_frame, borderwidth=2)

pdfPathLabel = tk.Label(frame_main_1, text = "Destino do PDF: ", font=("Helvetica 9 bold")).pack(side='left')

pathDestiny = tk.StringVar() # Para guardar a variavel path que vai ser definida na funçao browseButton

def browseButton():
    filename = filedialog.askdirectory()
    pathDestiny.set(filename)
    text = ''
    tk.Label(frame_main_1, text = filename[:45]).pack(side='left')
    return filename
buttonPath = tk.Button(frame_main_1, text="Destino", command=browseButton).pack(side='left')

frame_main_1.pack(fill='x', pady=2)

def run():
    if not pathDestiny.get():
        messagebox.showwarning("Informação", "Especifique o caminho de destino do PDF !")
    else:    
        print(pathDestiny.get())
        result = messagebox.askquestion("E-mail","Pretende enviar email para giovanna.magnante@gmail.com e fjnmgm@gmail.com ?")
        if result == 'yes':
            engine.run(pathDestiny.get().replace('/','\\'), True)
            messagebox.showinfo("E-mail enviado", "O email foi enviado para giovanna.magnante@gmail.com e fjnmgm@gmail.com")
        else: 
            engine.run(pathDestiny.get().replace('/','\\'))
            messagebox.showinfo("PDF gerado", f'O PDF foi gerado para {pathDestiny.get()}')
    

test = tk.Button(bottom_frame, text="Gerar PDF", command=run, bg='dark green', fg='white', relief='raised', width=20, font=('Helvetica 9 bold')).pack(side='left')



window.mainloop()


