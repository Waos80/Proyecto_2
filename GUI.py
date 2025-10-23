from automata import AFD
import analisis
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

def LeerArchivo(ruta: str) -> str:
    info = ""
    with open(ruta, "r") as f:
        info = f.read()

    return info

def findError(lexico: analisis.Lexico) -> bool:
    for token in lexico.tokens:
        if token[0] == "error":
            return True
        else:
            return False

def reporteErrores(lexico: analisis.Lexico) -> None:
    nerror = 0
    with open("Errores.html", "w", newline="\n") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='es'>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<title>Reporte de Errores</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }\n")
        f.write("table { border-collapse: collapse; width: 100%; background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }\n")
        f.write("caption { font-size: 1.5em; margin: 10px 0; font-weight: bold; color: #333; }\n")
        f.write("th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }\n")
        f.write("th { background-color: #6a0dad; color: white; }\n")
        f.write("table { border: 2px solid #6a0dad; }\n")
        f.write("tr:nth-child(even) { background-color: #f2f2f2; }\n")
        f.write("tr:hover { background-color: #e0e0e0; }\n")
        f.write("</style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<table>\n")
        f.write("<caption>Reporte de Errores</caption>\n")
        f.write("<tr>\n")
        f.write("<th>No.</th>\n")
        f.write("<th>Lexema</th>\n")
        f.write("<th>Tipo</th>\n")
        f.write("<th>Caracter</th>\n")
        f.write("<th>Fila</th>\n")
        f.write("</tr>\n")
        for token in lexico.tokens:
            if token[0] == "error":
                nerror += 1
                f.write("<tr>\n")
                f.write(f"<td>{nerror}</td>\n")
                f.write(f"<td>{token[1]}</td>\n")
                f.write(f"<td>{token[0]}</td>\n")
                f.write(f"<td>{token[2]}</td>\n")
                f.write(f"<td>{token[3]}</td>\n")
                f.write("</tr>\n")
        f.write("</table>\n")
        f.write("</body>\n")
        f.write("</html>\n")
    f.close()

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

def sigue_ejecucion(hilo: threading.Thread):
    if not hilo.is_alive():
        
        pass
    else:
        ventana.after(1000, sigue_ejecucion, hilo)

def analizar_codigo():
    pass

def analizar():
    global ruta_archivo
    error = False
    if ruta_archivo == None:
        messagebox.showerror("Archivo","No hay ningún archivo para analizar. \nSeleccione un archivo.")
        abrir_archivo()
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(texto.get("1.0", tk.END))
    info = LeerArchivo(ruta_archivo)

    digito = list("0123456789")
    OP = ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "POTENCIA", "RAIZ", "INVERSO", "MOD"]
        
    automata = analisis.AFD()
    automata.crearEstados(
        [False, False, False, True, 
        False, False, False, False, 
        False, False, False, True, 
        True, True, True, True]
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
            (OP, 8)
        ],
        5: [
            (["Operacion"], 9),
            (["Numero"], 10)
        ],
        6: [
            (['>'], 11)
        ],
        7: [
            (digito, 12)
        ],
        8: [
            (['>'], 13)
        ],
        9: [
            (['>'], 14)
        ],
        10: [
            (['>'], 15)
        ],
        12: [
            (digito, 12)
        ]
    })

    tabla = {
        3: "numero",
        11: "an",
        12: "numero",
        13: "ao",
        14: "co",
        15: "cn",
    }

    l = analisis.Lexico(automata, tabla)
    l.ProcesarEntrada(info)
    for token in l.tokens:
        if token[0] == "error":
            error = True
            break
    if not error:
        messagebox.showinfo("Ejecución","No se encontraron errores en el archivo de entrada. \nArchivo 'Resultados.html generado.")
    else:
        messagebox.showerror("Ejecución","Se encontraron errores en el archivo de entrada.\nArchivo 'Errores.html generado.")
        reporteErrores(l)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Editor de Archivos")
ventana.geometry("943x630")
ventana.resizable(False, False)

# Variable para guardar la ruta del archivo actual
ruta_archivo = None

# Frame superior con botones principales
frame_superior = tk.Frame(ventana)
frame_superior.pack(side="top", fill="x", padx=15, pady=5)

btn_Open = tk.Button(frame_superior, text="Abrir", command=abrir_archivo, height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_Open.pack(side="left", padx=4)

btn_Save = tk.Button(frame_superior, text="Guardar", command=guardar_archivo, height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_Save.pack(side="left", padx=4)

btn_SaveAs = tk.Button(frame_superior, text="Guardar Como", command=guardar_como, height = 3, width = 20, font = ("Arial", 10, "bold"))
btn_SaveAs.pack(side="left", padx=4)

btn_Analyze = tk.Button(frame_superior, text="Analizar", command = analizar, height = 3, width = 20, font = ("Arial", 10, "bold"))
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


