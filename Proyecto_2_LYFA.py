from automata import AFD
from analisis import Lexico
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Editor de Archivos")
ventana.geometry("943x630")
ventana.resizable(False, False)

# Variable para guardar la ruta del archivo actual
ruta_archivo = None

digito = list("0123456789")
OP = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "POTENCIA", "RAIZ", "INVERSO", "MOD"]
    
automata = AFD()
automata.crearEstados(
        [False, False, False, True, False, False, False, False, False, False, False, False, True, True, True, True, True]
    )

automata.crearTransiciones({
    0: [
        (['<'], 1),
        (['-'], 2),
        (digito, 3),
    ],
    1: [
        (["Operacion= "], 4),
        (['/'], 5),
        (["Numero"], 6),
    ],
    2: [
        (digito, 3)
    ],
    3: [
        (digito, 3),
        (['.'], 7)
    ],
    4: [
        #([' '], 4),
        (OP, 8)
    ],
    5: [
        #([' '], 9),
        (["Operacion"], 10),
        (["Numero"], 11)
    ],
    6: [
        #([' '], 6),
        (['>'], 12)
    ],
    7: [
        (digito, 13)
    ],
    8: [
        #([' '], 8),
        (['>'], 14)
    ],
    9: [
        #([' '], 9),
        (["Operacion"], 10)
    ],
    10: [
        #([' '], 10),
        (['>'], 15)
    ],
    11: [
        #([' '], 11),
        (['>'], 16)
    ],
    13: [
        (digito, 13)
    ],
})

tabla = {
    3: "numero",
    12: "an",
    13: "numero",
    14: "ao",
    15: "co",
    16: "cn"
}

lexico = Lexico(automata, tabla)

# Función para abrir archivo
def abrir_archivo() -> None:
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta_archivo:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            texto.delete("1.0", tk.END)
            texto.insert(tk.END, contenido)

# Función para guardar cambios
def guardar_archivo() -> None:
    global ruta_archivo
    if ruta_archivo == None:
        messagebox.showerror("Archivo", "Antes de guardar, debe de abrir un archivo para sobreescribir.")
        ruta_archivo = filedialog.askopenfilename(filetypes = [("Text files", "*.txt")])
    else:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Cambios guardados correctamente.")

# Función para guardar como nuevo archivo
def guardar_como() -> None:
    nueva_ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if nueva_ruta:
        with open(nueva_ruta, "w", encoding="utf-8") as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Archivo guardado como nuevo.")
        global ruta_archivo
        ruta_archivo = nueva_ruta

#Falta función para abrir el código 
#Falta función para correr el código

def sigue_ejecucion(hilo: threading.Thread):
    if not hilo.is_alive():
        
        pass
    else:
        ventana.after(1000, sigue_ejecucion, hilo)

def analizar_codigo():
    pass

def analizar():
    hilo = threading.Thread(target=analizar_codigo)
    hilo.start()
    ventana.after(1000, )

# Frame superior con botones principales
frame_superior = tk.Frame(ventana)
frame_superior.pack(side="top", fill="x", padx=15, pady=5)

btn_Open = tk.Button(frame_superior, text="Abrir", command=abrir_archivo, height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_Open.pack(side="left", padx=4)

btn_Save = tk.Button(frame_superior, text="Guardar", command=guardar_archivo, height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_Save.pack(side="left", padx=4)

btn_SaveAs = tk.Button(frame_superior, text="Guardar Como", command=guardar_como, height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_SaveAs.pack(side="left", padx=4)

btn_Analyze = tk.Button(frame_superior, text="Analizar", height = 3, width = 20, font = ("Arial", 10, "bold"))  # sin funcionalidad por ahora
btn_Analyze.pack(side="left", padx=4)

# Área de texto editable
frame_texto = tk.Frame(ventana)
frame_texto.pack(side = "left", padx= 10, pady= 10)
scroll_vertical = tk.Scrollbar(frame_texto)
scroll_vertical.pack(side= "right", fill= "y")
texto = tk.Text(frame_texto, wrap= "word", font= ("Arial", 12), height= 30, width= 79, yscrollcommand= scroll_vertical.set)
texto.pack(side = "left")
scroll_vertical.config(command = texto.yview)

# Frame lateral derecho con botones sin funcionalidad por ahora
frame_lateral = tk.Frame(ventana)
frame_lateral.pack(side="right", fill="y", padx=10, pady=10)

btn_UserManual = tk.Button(frame_lateral, text="Manual de Usuario", height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_UserManual.pack(pady = 5)

btn_TecnicManual = tk.Button(frame_lateral, text="Manual Técnico", height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_TecnicManual.pack(pady = 5)

btn_Help = tk.Button(frame_lateral, text="Ayuda", height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_Help.pack(pady = 5)

# Ejecutar la interfaz
ventana.mainloop()
