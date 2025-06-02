from tkinter import *
import tkinter.messagebox
from tkcalendar import DateEntry
import swag_datahandler as sdh


# Grundaufbau:
COLOR_THEME_1 = "green" # Farbe der Fenster & Label
COLOR_THEME_2 = "lime" # Farbe der Textfelder & mancher Buttons
TEXT_COLOR = "black"
BUTTON_FG_COLOR = "black"
swag = Tk()
swag.title("SWaG-Tool")
swag.configure(bg="black")
swag_frame = Frame(relief=RAISED,bd=8,bg=COLOR_THEME_1)
category = StringVar(swag_frame)



### Methoden:
# Methode, um Daten aus der gespeicherten json-Datei zu löschen
def erase_data():
    confirmed = tkinter.messagebox.askyesno(title="Eingabe leeren",message="Bist Du sicher?")
    if confirmed:
        print("Daten werden gelöscht...")
        file_name = category.get() + ".json"
        global datepicker_erase_from, datepicker_erase_until
        erase_from = datepicker_erase_from.get()
        erase_until = datepicker_erase_until.get()
        success = sdh.delete_from_Json_file(file_name, erase_from, erase_until)
        if not success:
            tkinter.messagebox.askokcancel(title="Eingabefehler", message="Fehler bei der Eingabe! Bitte überprüfe, ob das Datum unten weiter in der Zukunft liegt, als das Datum oben!")


# Methode, die nur float-Zahlen innerhalb eines "Entry" zulässt
def keylistener(inp):
    try:
        float(inp)
    except ValueError:
        return inp == ""
    else:
        return True


# Methode zum Aufruf eines Extra-Fensters zum Leeren aller Textfelder & Anzeigen
def erase_data_menu():

    # Untermethode, um das Extra-Fenster wieder zu schließen
    def close_window():
        top.destroy()
        top.update()

    print("Daten löschen gedrückt...")
    top = Toplevel(swag)
    top.configure(bg="black")
    top_frame = Frame(top, relief=RAISED,bd=8,bg=COLOR_THEME_1)

    # Label, Button:
    label_erase = Label(top_frame, text = "DATEN LÖSCHEN", font=30, background=COLOR_THEME_1, height=4)
    label_from = Label(top_frame, text = "VON:", background=COLOR_THEME_1, height=2)
    label_until = Label(top_frame, text = "BIS (inkl.):", background=COLOR_THEME_1, height=2)
    global datepicker_erase_from, datepicker_erase_until
    datepicker_erase_from = DateEntry(top_frame, width=12, background=COLOR_THEME_2, foreground=TEXT_COLOR, date_pattern="dd.mm.yyyy")
    datepicker_erase_until = DateEntry(top_frame, width=12, background=COLOR_THEME_2, foreground=TEXT_COLOR, date_pattern="dd.mm.yyyy")
    button_erase_data = Button(top_frame, bg="red",fg=TEXT_COLOR, text="Daten löschen", command=erase_data)
    button_close = Button(top_frame, bg="orange", fg=TEXT_COLOR, text="Fenster schließen", command=close_window)

    # Layout:
    top_frame.grid()
    label_erase.grid(columnspan=2)
    label_from.grid()
    label_until.grid()
    button_erase_data.grid(columnspan=2)
    button_close.grid(columnspan=2)
    datepicker_erase_from.grid(column=1, row=1)
    datepicker_erase_until.grid(column=1, row=2)


# Methode zum Bestätigen/Abspeichern
def save_as_json():
    json_file = category.get() + ".json"
    try:
        meter_value = float(input_meter_reading.get())
        date = datepicker.get()
        last_reading, last_date = update_last_reading()
        print(last_date, type(last_date))
        if(last_reading > meter_value):
            tkinter.messagebox.askokcancel(title="Messwert-Fehler", message="Es kann kein niedrigerer Wert als " + str(last_reading) + " eingegeben werden!")
            return
        check_date = sdh.check_dates(date, last_date)
        if not check_date:
            tkinter.messagebox.askokcancel(title="Datum-Fehler", message="Es kann kein niedrigeres oder gleiches Datum als das letzte Datum (" + last_date + ") eingegeben werden!")
            return
        new_entry = {
            "Datum": datepicker.get(),
            ("Zählerstand_" + category.get()): meter_value
        }
        print("Speichere...")
        sdh.save_To_Json_File(json_file, new_entry)
        update_last_reading()
        print("Speichern erfolgreich!")
    except(ValueError):
        error_message = "Bitte Gib in das Feld eine gültige Dezimalzahl ein (mit PUNKT, kein Text, kein Komma!)"
        print(error_message)
        error = tkinter.messagebox.askokcancel(title="FEHLER", message=error_message)

# Methode zur Ermittlung des letzten Zählerstands
def update_last_reading():
    data_name = category.get() + ".json"
    tmp_list_readings = sdh.read_data_from_file(data_name)
    if len(tmp_list_readings) == 0:
        print("Keine gefüllte Liste gefunden")
        label_info_last_reading["text"] = "---"
        default_date = "01.01.0001"
        return 0.0, default_date
    last_entry = tmp_list_readings[-1]
    reading_category = "Zählerstand_" + category.get()
    last_reading = last_entry[reading_category]
    print("Letzter Eintrag:", last_reading, type(last_reading))
    label_info_last_reading["text"] = last_reading
    last_date = last_entry["Datum"]
    return last_reading, last_date
    

# Methode zum richtigen Anzeigen der Einheit:
def update_unit(event):
    if (category.get() == "Strom" or category.get() == "Heizstrom"):
        label_unit["text"] = "kWh"
        label_unit_2["text"] = "kWh"
    else:
        label_unit["text"] = "m³"
        label_unit_2["text"] = "m³"
    update_last_reading()

# GUI-Methode zum Anzeigen des Graphen (Linien-Diagramm)
def show_graph_gui():
    tmp_category = category.get()
    print("Zeige Zählerstand", tmp_category, "..." )
    sdh.show_graph(tmp_category)

# GUI-Methode zum Anzeigen des Verbrauchs (Balken-diagramm)
def show_consumption_gui():
    tmp_category = category.get()
    print("Zeige Verbrauch", tmp_category, "...")
    sdh.show_consumption(tmp_category)

# Labels:
label_title = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="SWAG-Tool", font=30, height=4)
label_category = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="Kategorie:", height=2)
label_date = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="Datum:", height=2)
label_meter_graph = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="Zählerstand:", height=2)
label_seperator = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="-----------------------------------", height=2)
label_last_reading = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="Letzter Zählerstand: ")
label_info_last_reading = Label(swag_frame, bg=COLOR_THEME_2, fg=TEXT_COLOR, text="")
label_unit = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="kWh")
label_unit_2 = Label(swag_frame, bg=COLOR_THEME_1, fg=TEXT_COLOR, text="kWh")

# Drop-Down-Menu
category.set("Strom")
categories = ["Strom", "Wasser", "Gas", "Heizstrom"]
category_menu = OptionMenu(swag_frame, category, *categories, command=update_unit)

# Datums- & Textfelder:
datepicker = DateEntry(swag_frame, width=12, background=COLOR_THEME_2, foreground=COLOR_THEME_2, date_pattern="dd.mm.yyyy")
input_meter_reading = Entry(swag_frame,bg=COLOR_THEME_2,fg=COLOR_THEME_2)

# Start Keylistener
allow_only_numbers = swag.register(keylistener)
input_meter_reading.config(validate="key", validatecommand=(allow_only_numbers, "%P"))

# Buttons:
button_erase = Button(swag_frame,bg="red",fg=BUTTON_FG_COLOR, text="Zählerstände löschen...", command=erase_data_menu)
button_save = Button(swag_frame,bg="orange", fg="white", text="Speichere Daten...", command=save_as_json)
button_show_graph = Button(swag_frame, bg=COLOR_THEME_2, fg=BUTTON_FG_COLOR, text="Plot Zählerstand", command=show_graph_gui)
button_show_consumption = Button(swag_frame, bg=COLOR_THEME_2, fg=BUTTON_FG_COLOR, text="Plot Verbrauch", command=show_consumption_gui)

# Baue Umgebung:
swag_frame.grid()
# Labels
label_title.grid(column=0,row=0, columnspan=4)
label_category.grid(column=0, row=2)
label_date.grid(column=0, row=3)
label_meter_graph.grid(column=0, row=4)
label_seperator.grid(column=0,row=5,columnspan=4)
label_last_reading.grid(column=0, row=6)
label_info_last_reading.grid(column=1, row=6)
label_unit.grid(column=2, row=4)
label_unit_2.grid(column=2, row=6)
# Eingabe-Felder
category_menu.grid(column=1, row=2)
datepicker.grid(column=1, row=3)
input_meter_reading.grid(column=1, row=4)
# Buttons
button_save.grid(column=0, row=8, pady=10, padx=20, columnspan=4)
button_erase.grid(column=0, row=9, columnspan=4)
button_show_graph.grid(column = 0, row=10, pady=10, padx= 20, columnspan=2)
button_show_consumption.grid(column = 2, row=10, pady=10, padx= 20, columnspan=2)

# Update_event
swag.after(1, update_last_reading)

# Starte Programm
swag.mainloop()