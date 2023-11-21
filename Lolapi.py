try:
    import requests
    import tkinter as tk
    from tkinter import Label, PhotoImage, Canvas, Scrollbar
    from PIL import Image, ImageTk
except ImportError as e:
    print(f"Error al importar una o más librerías: {e}")
    print("Se procederá a instalar las librerías faltantes.")

    try:
        import subprocess
        subprocess.check_call(["pip", "install", "requests", "tkinter", "Pillow"])
        print("Librerías instaladas correctamente.")
        import requests
        import tkinter as tk
        from tkinter import Label, PhotoImage, Canvas, Scrollbar
        from PIL import Image, ImageTk
    except Exception as install_error:
        print(f"No se pudieron instalar las librerías. Error: {install_error}")
        exit()
import requests
import tkinter as tk
from tkinter import Label, PhotoImage, Canvas, Scrollbar
import io
from PIL import Image, ImageTk
import random

# URL de la API de League of Legends
api_url = "https://ddragon.leagueoflegends.com/cdn/13.23.1/data/en_US/champion.json"

# Realizar la solicitud GET a la API
response = requests.get(api_url)

# Obtener datos de campeones desde la respuesta JSON
champion_data = response.json()["data"]

# Obtener nombres de campeones
champion_names = list(champion_data.keys())

# Función para mostrar un campeón específico
def mostrar_campeon(campeon):
    # Obtener datos del campeón seleccionado
    campeon_data = champion_data[campeon]
    nombre = campeon_data["name"]
    imagen_url = f"https://ddragon.leagueoflegends.com/cdn/13.23.1/img/champion/{campeon_data['image']['full']}"

    # Actualizar la etiqueta con el nombre del campeón
    nombre_label.config(text=nombre)

    # Descargar la imagen desde la URL
    response_image = requests.get(imagen_url)
    image_data = io.BytesIO(response_image.content)
    image = Image.open(image_data)

    # Convertir la imagen a PhotoImage
    photo = ImageTk.PhotoImage(image)

    # Actualizar la etiqueta con la imagen del campeón
    imagen_label.config(image=photo)
    imagen_label.image = photo

# Función para mostrar un campeón aleatorio
def mostrar_campeon_aleatorio():
    campeon = random.choice(champion_names)
    mostrar_campeon(campeon)

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Campeones de League of Legends")

# Etiqueta para mostrar el nombre del campeón
nombre_label = Label(ventana, text="", font=("Helvetica", 16))
nombre_label.pack(pady=10)

# Etiqueta para mostrar la imagen del campeón
imagen_label = Label(ventana)
imagen_label.pack(pady=10)

# Botón para obtener un campeón aleatorio
boton_obtener_campeon = tk.Button(ventana, text="Obtener Campeón Aleatorio", command=mostrar_campeon_aleatorio)
boton_obtener_campeon.pack(pady=10)

# Canvas para organizar los botones y agregar un Scrollbar
canvas = Canvas(ventana)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar para el Canvas
scrollbar = Scrollbar(ventana, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configurar el Canvas para que sea desplazable
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Frame dentro del Canvas para los botones
frame_botones = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_botones, anchor="nw")

# Botones para mostrar todos los campeones en una cuadrícula
row = 0
col = 0
for campeon in champion_names:
    boton_campeon = tk.Button(frame_botones, text=campeon, command=lambda c=campeon: mostrar_campeon(c))
    boton_campeon.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Ejecutar la interfaz gráfica
ventana.mainloop()
