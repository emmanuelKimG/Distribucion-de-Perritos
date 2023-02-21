from tkinter import *
from tkinter import ttk
from tkinter.tix import *
import matplotlib.pyplot as plt
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import pandas as pd
import numpy as np


def select_file():
    global file
    try:
        file_downloaded = fd.askopenfile(initialdir="/Downloads" ,filetypes=[('CSV Files', '*.csv')])
        file = pd.read_csv(file_downloaded)

        file['edad'] = pd.to_numeric(file['edad'])
        file["raza"] = file["raza"].str.strip()
        grouped = file.groupby('raza')['edad'].mean().reset_index()
        
        # Crear una figura y un eje para la gráfica
        fig, ax = plt.subplots()
        checkbox_vars = {}
        unique_raza = grouped['raza'].unique()
        
        checkbox_window = Toplevel(root)
        checkbox_frame = ttk.Frame(checkbox_window, padding=10)
        checkbox_frame.pack(side="left", fill="y")

        canvas = Canvas(checkbox_window)
        scrollbar = ttk.Scrollbar(checkbox_window, orient=VERTICAL, command=canvas.yview)
        checkbox_frame_inner = ttk.Frame(canvas)
        checkbox_frame_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=checkbox_frame_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Creamos un checkbox por cada nombre diferente de raza 
        for raza in unique_raza.tolist():   
            checkbox_vars[raza] = BooleanVar()
            ttk.Checkbutton(checkbox_frame_inner, text=raza, variable=checkbox_vars[raza]).pack()

        # Agregamos el scroll a la venatana de checkboxes
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
    
        # Obtnener los checkboxes seleccionados 
        def get_selected():
            ax.clear()
            selected = []
            for raza in checkbox_vars:
                if checkbox_vars[raza].get():
                    selected.append(raza)
                    print(raza)

            # Iterar por cada raza y crear una distribución normal para la edad
            for raza in selected:
                data = file[file['raza'] == raza]['edad']
                mean = data.mean()
                std = data.std()
                print(f"{data} Mean {mean} std = {std}" )
                x = np.linspace(mean - 3 * std, mean + 3 * std, 100)
                y = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / std) ** 2)
                label = f"{raza}"
                ax.plot(x, y, label=label)

            ax.legend()
            ax.set_xlabel('Edad')
            ax.set_ylabel('Densidad de probabilidad')
            ax.set_title('Distribución de la edad por raza')
            plt.show()

        ttk.Button(canvas, text="Get Selected", command=get_selected).pack() 

        checkbox_frame.pack()
    
    except FileNotFoundError:
        mb.showerror(message="File not found.")
    except pd.errors.EmptyDataError:
        mb.showerror(message="No data")
    except pd.errors.ParserError:
        mb.showerror(message="Parse error")
    except Exception:
        mb.showerror(message= "Lo siento viejo, el archivo que subiste esta malito")
        

         
root = Tk()
frame = ttk.Frame(root,padding = 10)
root.geometry("500x200")
root.title("Grafica de Perritos")
ttk.Label(frame, text="SELECCIONE UN ARCHIVO TIPO CSV",padding=30).pack()
ttk.Button(frame, text="Telecharger", command=select_file).pack()
ttk.Button(frame, text="Quiter", command=root.destroy).pack()

frame.pack(side="top")
root.mainloop()


