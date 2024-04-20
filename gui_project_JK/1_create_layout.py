# Layout
import tkinter.ttk as ttk
from tkinter import *

root = Tk()
root.title("JK Photo Merge")

# 1) Datei-Frame (Datei hinzufügen, Auswahl löschen)
file_frame = Frame(root)
file_frame.pack(fill = "x", padx = 5, pady = 5) # padding (Abstand) hinzufügen

btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "Datei hinzufügen")
btn_add_file.pack(side = "left")

btn_del_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "Auswahl löschen")
btn_del_file.pack(side = "right")

# Listen-Frame & Scrollbar
list_frame = Frame(root)
list_frame.pack(fill = "both", padx = 5, pady = 5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = "right", fill = "y")

list_file = Listbox(list_frame, selectmode = "extended", height = 15, yscrollcommand = scrollbar.set)
list_file.pack(side = "left", fill = "both", expand = True)
scrollbar.config(command = list_file.yview)

# Speicherpfad-Frame
path_frame = LabelFrame(root, text = "Speicherpfad")
path_frame.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

txt_dest_path = Entry(path_frame) # Wenn es sich um ein Text-Widget gehandelt hätte, dann "1.0", END
txt_dest_path.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5, ipady = 4) # ipady: Höhe ändern

button_dest_path = Button(path_frame, text = "Durchsuchen", width = 10)
button_dest_path.pack(side = "right", padx = 5, pady = 5)

# Optionen-Frame
frame_option = LabelFrame(root, text = "Optionen")
frame_option.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

# Breitenoption
# Breiten-Label
label_width = Label(frame_option, text = "Breite", width = 8)
label_width.pack(side = "left", padx = 5, pady = 5) # side = "left" verhindert vertikales Stapeln

# Breiten-Combobox
option_width = ["Original", "1024", "800", "640"]
combo_width = ttk.Combobox(frame_option, state = "readonly", values = option_width, width = 10)
combo_width.current(0)
combo_width.pack(side = "left", padx = 5, pady = 5)

# Abstandsoption
# Abstand-Label
label_space = Label(frame_option, text = "Abstand", width = 8)
label_space.pack(side = "left", padx = 5, pady = 5)

# Abstands-Combobox
option_space = ["Kein", "Schmal", "Normal", "Breit"]
combo_space = ttk.Combobox(frame_option, state = "readonly", values = option_space, width = 10)
combo_space.current(0)
combo_space.pack(side = "left", padx = 5, pady = 5)

# Dateiformat-Optionen
# Dateiformat-Label
label_format = Label(frame_option, text = "Format", width = 8)
label_format.pack(side = "left", padx = 5, pady = 5)

# Dateiformat-Combobox
option_format = ["PNG", "JPG", "BMP"]
combo_format = ttk.Combobox(frame_option, state = "readonly", values = option_format, width = 10)
combo_format.current(0)
combo_format.pack(side = "left", padx = 5, pady = 5)

# Fortschrittsanzeige : Progress Bar
frame_progress = LabelFrame(root, text = "Fortschritt")
frame_progress.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(frame_progress, maximum = 100, variable = p_var)
progressbar.pack(fill = "x")

# Ausführungsframe
frame_run = Frame(root)
frame_run.pack(fill = "x", padx = 5, pady = 5)

btn_close = Button(frame_run, padx = 5, pady = 5,  text = "Schließen", width = 12, command = root.quit)
btn_close.pack(side = "right", padx = 5, pady = 5)

btn_start = Button(frame_run, padx = 5, pady = 5, text = "Start", width = 12)
btn_start.pack(side = "right", padx = 5, pady = 5)

root.resizable(False, False)
root.mainloop() # verhindert, dass das Fenster geschlossen wird