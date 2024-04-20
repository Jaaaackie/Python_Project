import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image

root = Tk()
root.title("JK Photo Merge")

def add_file():
    files = filedialog.askopenfilenames(title = "Wählen Sie Bilddateien aus",
                                        filetypes = (("PNG Datei", "*.png"), ("Alle Dateien", "*.*")),
                                        initialdir = r"C:\Users\jeong\Desktop\PythonWorkspace")

    for file in files:
        print(file)
        list_file.insert(END, file)

def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected is None:
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# Bilder zu einer Datei zusammenfügen
def merge_images():
    # print(list_file.get(0, END)) # Alle Dateien auflisten
    images = [Image.open(x) for x in list_file.get(0, END)]
    
    # Erklärung :
    # size -> size[0] : Breite, size[1] : Höhe
    # Um Bilder zusammenzufügen, muss man die breiteste Breite und die gesamte Höhe der kombinierten Bilder kennen
    # widths = [x.size[0] for x in images]
    # heights = [x.size[1] for x in images]
    # # -> (widths, heights) = [(10, 10), (20, 20), (40, 40), ..]

    # Das gleiche Ergebnis wie oben, aber einfacher ausgedrückt mit zip, unzip(=zip(*()))
    widths, heights = zip(*(x.size for x in images))

    # Die maximale Breite und die gesamte Höhe der Bilder ermitteln    
    max_width, total_height = max(widths), sum(heights)

    # Skizzenbuch vorbereiten, um die zusammengefügten Bilder zu zeichnen
    result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255)) # Hintergrund : Weiß
    y_offset = 0 # x-Koordinat bleibt unändert, nur y-Koordinate verschiebt sich: y-Position
    
    for idx, img in enumerate(images):
        result_img.paste(img, (0, y_offset))
        y_offset += img.size[1] # Höhe zum y-offset hinzufügen

        progress = (idx + 1) / len(images) * 100 # Echten Prozentwert berechnen
        p_var.set(progress)
        progressbar.update()

    dest_path = os.path.join(txt_dest_path.get(), "jk_merged.jpg")
    result_img.save(dest_path)
    msgbox.showinfo("Benachrichtigung", "Die Arbeit ist abgeschlossen.")

def start():
    print("Breite : ", combo_width.get())
    print("Abstand : ", combo_space.get())
    print("Format :", combo_format.get())

    if list_file.size() == 0:
        msgbox.showwarning("Warnung", "Bitte fügen Sie Bilddateien hinzu")
        return
    
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warnung", "Bitte wählen Sie einen Speicherpfad aus")
        return

    merge_images()

file_frame = Frame(root)
file_frame.pack(fill = "x", padx = 5, pady = 5)

btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "Datei hinzufügen", command = add_file)
btn_add_file.pack(side = "left")

btn_del_file = Button(file_frame, padx = 5, pady = 5, width = 12, text = "Auswahl löschen", command = del_file)
btn_del_file.pack(side = "right")

list_frame = Frame(root)
list_frame.pack(fill = "both", padx = 5, pady = 5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = "right", fill = "y")

list_file = Listbox(list_frame, selectmode = "extended", height = 15, yscrollcommand = scrollbar.set)
list_file.pack(side = "left", fill = "both", expand = True)
scrollbar.config(command = list_file.yview)

path_frame = LabelFrame(root, text = "Speicherpfad")
path_frame.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5, ipady = 4)

button_dest_path = Button(path_frame, text = "Durchsuchen", width = 10, command = browse_dest_path)
button_dest_path.pack(side = "right", padx = 5, pady = 5)

frame_option = LabelFrame(root, text = "Option")
frame_option.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

label_width = Label(frame_option, text = "Breite", width = 8)
label_width.pack(side = "left", padx = 5, pady = 5)

option_width = ["Original", "1024", "800", "640"]
combo_width = ttk.Combobox(frame_option, state = "readonly", values = option_width, width = 10)
combo_width.current(0)
combo_width.pack(side = "left", padx = 5, pady = 5)

label_space = Label(frame_option, text = "Abstand", width = 8)
label_space.pack(side = "left", padx = 5, pady = 5)

option_space = ["Kein", "Schmal", "Normal", "Breit"]
combo_space = ttk.Combobox(frame_option, state = "readonly", values = option_space, width = 10)
combo_space.current(0)
combo_space.pack(side = "left", padx = 5, pady = 5)

label_format = Label(frame_option, text = "Format", width = 8)
label_format.pack(side = "left", padx = 5, pady = 5)

option_format = ["PNG", "JPG", "BMP"]
combo_format = ttk.Combobox(frame_option, state = "readonly", values = option_format, width = 10)
combo_format.current(0)
combo_format.pack(side = "left", padx = 5, pady = 5)

frame_progress = LabelFrame(root, text = "Fortschritt")
frame_progress.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(frame_progress, maximum = 100, variable = p_var)
progressbar.pack(fill = "x")

frame_run = Frame(root)
frame_run.pack(fill = "x", padx = 5, pady = 5)

btn_close = Button(frame_run, padx = 5, pady = 5,  text = "Schließen", width = 12, command = root.quit)
btn_close.pack(side = "right", padx = 5, pady = 5)

btn_start = Button(frame_run, padx = 5, pady = 5, text = "Start", width = 12, command = start)
btn_start.pack(side = "right", padx = 5, pady = 5)

root.resizable(False, False)
root.mainloop()