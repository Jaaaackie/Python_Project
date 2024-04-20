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
        list_file.insert(END, file)

def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    # "if folder_selected is None" bedeutet: der Benutzer wählt keinen Pfad aus und klickt auf Abbrechen
    # Bug) Wenn ein Pfad ausgewählt und dann erneut ein Pfad ausgewählt und abgebrochen wird, verschwindet der Pfad
    if folder_selected == '': # Bugfix
        # print("Ordnerauswahl abgebrochen")
        msgbox.showinfo("Benachrichtigung", "Ordnerauswahl abgebrochen")

        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

def merge_images():

    # Bug 1) In Windows 10 ist zum Erstellen von Dateien auf dem C-Laufwerk eine Berechtigung erforderlich, die dieses Programm nicht hat.
        # Es sollte dann eine Fehlermeldung erscheinen, aber nicht.
    # Bug 2) Wenn ein nicht vorhandenes Laufwerk als Pfad ausgewählt wird, sollte eine Fehlermeldung erscheinen, aber auch nicht.
    # Bugfix) (try: ... except)
    try:
        # Breite
        img_width = combo_width.get()
        if img_width == "Original":
            img_width = -1 # -1 : Das Bild wird basierend auf die Originalbilder zusammengefügt
        else:
            img_width = int(img_width) # Da die Option eine Zahl ist, in "int" umwandeln

        # Abstand
        img_space = combo_space.get()
        if img_space == "Schmal":
            img_space = 30 # Einen Abstand von 30 zwischen den Bildern einfügen
        
        elif img_space == "Normal":
            img_space = 60
        
        elif img_space == "Breit":
            img_space = 90
        
        else: # Option "Kein"
            img_space = 0

        # Format
        img_format = combo_format.get().lower() # Werte für PNG, JPG, BMP in Kleinbuchstaben umwandeln

        ################################

        images = [Image.open(x) for x in list_file.get(0, END)]

        # Bildgrößen in eine Liste einfügen und einzeln verarbeiten
        image_sizes = [] # [(width1, height1), (width2, height2), ...]
        
        if img_width > -1:
            # Wenn die Option zur Änderung der Bildbreite der zusammengefügten Bildern nicht "Kein" (img_width = -1) ist, muss die Breite geändert werden
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]

        else:
            image_sizes = [(x.size[0], x.size[1]) for x in images] # Originalgröße verwenden

        # Mit zip(*) Tupel trennen
        widths, heights = zip(*image_sizes)

        # Maximale Breite und Gesamthöhe der Bilder ermitteln    
        max_width, total_height = max(widths), sum(heights)

        # Skizzenbuch vorbereiten, um die zusammengefügten Bilder zu zeichnen
        if img_space > 0: # Bei der Zusammenführung der Bildern die Option für den Bildabstand anwenden
            total_height += (img_space * (len(images) -1)) # (len(images) - 1), also Gesamtzahl der Bildern - 1 wegen des Abstands 

        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0
        
        for idx, img in enumerate(images):
            # Wenn die Option für Breite nicht "Original" gewählt ist, muss die Bildgröße angepasst werden
            if img_width > -1:

                # "image_sizes" ist eine Liste,
                # und diese Liste enthält für jedes Bild der len(images) Bilder jeweils Breite und Höhe.
                # Wenn der Index des aktuellen Bildes eingefügt wird, erhalten wir die geänderte Bildgröße für dieses Bild (resizing)
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_space) # Änderung die y-Position auf (Höhe des hinzugefügten Bildes + gewählte Abstandoption)

            progress = (idx + 1) / len(images) * 100
            p_var.set(progress)
            progressbar.update()

        # Option für Format & Dateinamen verarbeiten
        file_name = "jk_merged_{}_{}.".format(combo_width.get(), combo_space.get()) + img_format

        dest_path = os.path.join(txt_dest_path.get(), file_name)

        result_img.save(dest_path)
        msgbox.showinfo("Benachrichtigung", "Die Arbeit ist abgeschlossen")

    except Exception as err:
        # Ausnahmebehandlung, es ist schwierig, jeden Fehler einzeln zu behandeln, also alles zusammenfassen -> Exception

        msgbox.showerror("Error", err)

def start():
    if list_file.size() == 0:
        msgbox.showwarning("Warnung", "Fügen Sie bitte Bilddatei hinzu")
        return
    
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warnung", "Wählen Sie bitte einen Speicherpfad aus")
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