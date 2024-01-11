import json
import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import date
import re

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = params = {
    "latitude": 32.3329,
    "longitude": 34.8599,
    "current": "european_aqi",
    "timezone": "auto"}
response = requests.get(url, params)
status_response = response.status_code
data = response.json()


# table of european aqi interpretation
# Note: The European Air Quality Index (AQI) ranges from 0-20 (good), 20-40 (fair), 40-60 (moderate), 60-80 (poor), 80-100 (very poor) and exceeds 100 for extremely poor conditions.


def analize_data():
    if status_response != 200:
        return 'No es posible conectarse , intente de nuevo'
    full_time = data["current"]["time"]
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})')
    date_search_results = re.search(pattern, full_time)
    date = date_search_results.group(1)
    date_list = date.split('-')
    date_list.reverse()
    date = '-'.join(date_list)
    hour = date_search_results.group(2)
    air_quality = data["current"]["european_aqi"]
    if air_quality >= 0 and air_quality < 20:
        calidad = "EXCELENTE"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'
    elif air_quality >= 20 and air_quality < 40:
        calidad = "BUENA"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'
    elif air_quality >= 40 and air_quality < 60:
        calidad = "REGULAR"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'
    elif air_quality >= 60 and air_quality < 80:
        calidad = "MALA"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'
    elif air_quality >= 80 and air_quality < 100:
        calidad = "MUY MALA"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'
    elif air_quality >= 0 and air_quality < 20:
        calidad = "EXCELENTE"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'
    elif air_quality >= 100:
        calidad = "EXTREMADAMENTE MALA,CUIDADO"
        return f'HORA: {hour}; FECHA: {date}; \n\nCALIDAD DEL AIRE: INDICE {air_quality}  ,  {calidad}'


def set_text():
    final_text = text.set(analize_data())
    return final_text


root = tk.Tk()
root.geometry('750x200')
root.resizable(False, False)
root.title('AIR INDEX APP')
section = ttk.Frame(root)
section.pack()

text = tk.StringVar(
    value="HAZ CLICK PARA OBTENER DATOS DEL SATELITE\n            ACTUALIZACIONES CADA HORA")
label = ttk.Label(section, text="APP EDUA CALIDAD DEL AIRE", font=("Roboto", 12),
                  anchor='center', padding=3)
label.pack(pady=9)
label2 = ttk.Label(section, textvariable=text, font=("Roboto", 12),
                   anchor='center', padding=3)
label2.pack(pady=8)

button = ttk.Button(section, padding=6, command=set_text,
                    text="CLICK AQUI", cursor="hand2")
button.pack(pady=6)


root.mainloop()
