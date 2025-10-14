import tkinter as tk
from tkinter import filedialog, messagebox

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Editor de Archivos")
ventana.geometry("943x630")
ventana.resizable(False, False)

# Variable para guardar la ruta del archivo actual
ruta_archivo = None

# Función para abrir archivo
def abrir_archivo():
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta_archivo:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
            texto.delete("1.0", tk.END)
            texto.insert(tk.END, contenido)

# Función para guardar cambios
def guardar_archivo():
    global ruta_archivo
    if ruta_archivo == None:
        messagebox.showerror("Archivo", "Antes de guardar, debe de abrir un archivo para sobreescribir.")
        ruta_archivo = filedialog.askopenfilename(filetypes = [("Text files", "*.txt")])
    else:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Cambios guardados correctamente.")

# Función para guardar como nuevo archivo
def guardar_como():
    nueva_ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if nueva_ruta:
        with open(nueva_ruta, "w", encoding="utf-8") as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Archivo guardado como nuevo.")
        global ruta_archivo
        ruta_archivo = nueva_ruta

#Falta función para abrir el código 
#Falta función para correr el código

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
