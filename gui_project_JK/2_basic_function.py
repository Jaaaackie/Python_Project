# Dateien hinzufügen, um sie in die Listbox einzufügen, 
# und dann ausgewählte Einträge daraus löschen, Speicherpfad-Funktion implemetieren
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
    # 2) Wenn Untermodule in __all__ nicht definiert ist, werden sie nicht importiert, deshalb muss "filedialog" zusätzlich importiert werden

root = Tk()
root.title("JK Photo Merge")

# Dateien hinzufügen : ein Dateidialog öffnet, um zu fragen, welche Dateien in welchen Pfad ausgewählt werden sollen
def add_file():
    files = filedialog.askopenfilenames(title = "Wählen Sie Bilddateien aus",
                                        filetypes = (("PNG Datei", "*.png"), ("Alle Dateien", "*.*")),
                                        initialdir = r"C:\Users\jeong\Desktop\PythonWorkspace\pygame_project\images")
    # Zeigt den anfänglich vom Benutzer angegebenen Pfad an: r"Pfad" bedeutet, dass Escape-Zeichen ignoriert werden und der pfand so verwendet wird, wie er geschrieben ist

    # Liste der vom Benutzer ausgewählten Dateien
    for file in files:
        print(file)
        list_file.insert(END, file)

# Auswahl löschen
def del_file():
    # print(list_file.curselection())
    # for index in list_file.curselection():
    #     list_file.delete(index)
        
    # Verwenden von "reversed", um die Indizes rückwärts zu durchlaufen, 
    # verhindert das Problem, dass beim Löschen der Datei an Index 0 die darunterliegende Datei nach oben rutscht und wieder Index 0 wird
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# Speicherpfad (Ordner) auswählen
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected is None: # Wenn der Benutzer keinen Pfad auswählt und auf Abbrechen klickt
        return
    # print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# Start 
def start():
    # Überprüfung der Werte der einzelenen Optionen
    print("Breite : ", combo_width.get())
    print("Abstand : ", combo_space.get())
    print("Format :", combo_format.get())

    # Überprüfung der Dateiliste
    if list_file.size() == 0: # Falls keine Dateien hinzugefügt wurden
        msgbox.showwarning("Warnung", "Bitte fügen Sie Bilddateien hinzu")
        return
    
    # Überprüfung des Speicherpfads
    if len(txt_dest_path.get()) == 0: # Dass die Länge des Strings 0 ist, bedeutet, dass kein Speicherpfad festgelegt wurde
        msgbox.showwarning("Warnung", "Bitte wählen Sie einen Speicherpfad aus")
        return

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