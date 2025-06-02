import json, os
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# False, wenn date_1 < date_2
# True,  wenn date_1 > date_2

def check_dates(date_1, date_2):
    date_to_check = dt.datetime.strptime(date_1, "%d.%m.%Y").date()
    date_threshold = dt.datetime.strptime(date_2, "%d.%m.%Y").date()
    if date_threshold >= date_to_check:
        return False
    return True

def change_color_unit(category):
     # Fallunterscheidung:
    if category == "Strom":
        return "orange", "(kWh)"
    elif category == "Wasser":
        return "cyan", "(m³)"
    elif category == "Heizstrom":
        return "red", "(kWh)"
    elif category == "Gas":
        return "green", "(m³)"
    return "black", "(kWh)"

def read_data_from_file(data_name) -> list:
    try:
        path_to_file = os.path.join(os.getcwd(),"data",data_name)
        with open(path_to_file, "r", encoding="UTF-8") as json_data:
            return json.load(json_data)
    except(FileNotFoundError):
        print("Datei", data_name, "nicht gefunden")
        return []

def save_To_Json_File(data_name, new_entry, override = False):
    path_to_file = os.path.join(os.getcwd(),"data")
    if not os.path.exists(path_to_file):
        print("Ordner existiert nicht! Erstelle Ordner...")
        os.mkdir(path_to_file)
    path_to_file = os.path.join(path_to_file, data_name)
    date = None
    if override:
        print("Datei wird komplett überschrieben!")
        data = new_entry
    else:
        if not os.path.exists(path_to_file):
            print("Datei existiert nicht, erstelle Datei...")
            data = [new_entry]
        else:
            print("Datei existiert, erweitere Datei...")
            data = read_data_from_file(data_name)
            data.append(new_entry)
    with open(path_to_file, "w", encoding="UTF-8") as json_data:
        json.dump(data, json_data, indent=4)

1
def delete_from_Json_file(data_name, delete_from, delete_until):
    current_data = read_data_from_file(data_name)
    if current_data == []:
        print("Leere Liste, es gibt nichts zu löschen")
        return
    print(current_data)
    date_delete_from = dt.datetime.strptime(delete_from, "%d.%m.%Y").date()
    date_delete_until = dt.datetime.strptime(delete_until, "%d.%m.%Y").date()
    tmp_element = current_data[0]
    tmp_element_date = dt.datetime.strptime(tmp_element.get("Datum"), "%d.%m.%Y").date()
    print("Erster Eintrag (Datum):", tmp_element_date, type(tmp_element_date))
    # Check: Datumseingabe oben mus <= unten sein!
    if (date_delete_until < date_delete_from):
        return False
    # Randfall: Nur 1 Element in der Liste:
    if len(current_data) == 1:
        print("ACHTUNG: Nur 1 Element in der Liste! Nach dieser Aktion ist die Liste leer")
        current_data.remove(tmp_element)
    else:
        # Schleife:
        while (date_delete_from <= tmp_element_date) and (tmp_element_date <= date_delete_until):
            print("Element wird gelöscht!")
            current_data.remove(tmp_element)
            tmp_element = current_data[0]
            tmp_element_date = dt.datetime.strptime(tmp_element.get("Datum"), "%d.%m.%Y").date()
            print("Neuer Erster Eintrag (Datum): ", tmp_element_date)
    print("Löschen war erfolgreich!")
    save_To_Json_File(data_name, current_data, override=True)
    return True
        

def show_graph(category):
    # y-Achse Zählerstand in kWh oder m³
    # x-Achse Zeitstrahl
    # Falls offen: schließe alten Plot
    plt.close()
    category_color, category_unit = change_color_unit(category)

    date = []
    meter_reading = []

    data_list = read_data_from_file(category + ".json")
    element_name = "Zählerstand_" + category
    
    for element in data_list:
        date.append(element["Datum"])
        meter_reading.append(element[element_name])

    x_data = [dt.datetime.strptime(d, "%d.%m.%Y").date() for d in date]
    y_data = meter_reading
    font = {"family":"serif", "color":"green", "size": 20}

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
    plt.plot(x_data, y_data, color=category_color, marker="o")
    plt.gcf().autofmt_xdate()
    plt.title((category + "zählerstand"), fontdict=font)
    plt.ylabel("Zählerstand " + category_unit, fontdict=font)
    plt.xlabel("Datum", fontdict=font)
    plt.legend([category])
    for x, y in zip(x_data, y_data):
        plt.annotate(str(y), [x, y + 10.0])
    plt.show()


def show_consumption(category):
    # Falls offen: schließe alten Plot
    plt.close()

    data_list = read_data_from_file(category + ".json")

    consumption = []
    date = []

    if data_list != []:
        tmp_reading_before = 0
        tmp_reading_after = data_list[0]["Zählerstand_" + category]
        for element in data_list:
            date.append(element["Datum"])
            tmp_reading_before = tmp_reading_after
            tmp_reading_after = element["Zählerstand_" + category]
            consumption.append((tmp_reading_after - tmp_reading_before))

    print(consumption)
    print(date)

    y = consumption
    x = date
    category_color, category_unit = change_color_unit(category)

    font = {"family":"serif", "color":"blue", "size": 20}
    fig, ax = plt.subplots()

    ax_bar_category = plt.bar(x, y,color=category_color)
    plt.xticks(rotation='vertical')
    plt.xlabel("Datum", fontdict=font)
    plt.ylabel("Verbrauch" + category_unit, fontdict=font)
    ax.bar_label(ax_bar_category)
    plt.legend([category])
    plt.show()

if __name__ == "__main__":
    current_data = read_data_from_file("Strom.json")
    print(type(current_data))
    print(current_data, type(current_data))
    feb_29_2020 = "29.02.2020"
    mar_01_2020 = "01.03.2020"
    feb_29_2024 = "29.02.2024"
    dec_31_2020 = "31.12.2020"
    print("Der 29. Februar 2020 kommt vor dem 01.März 2020:", check_dates(mar_01_2020, feb_29_2020))
    print("Der 29. Februar 2024 kommt nach dem 01.März 2020:", check_dates(feb_29_2020, mar_01_2020))
    print("Der 29. Februar 2020 kommt vor dem 31.Dezember 2020:", check_dates(dec_31_2020, feb_29_2020))
    print("Der 29. Februar 2024 kommt vor dem 31.Dezember 2020:", check_dates(dec_31_2020, feb_29_2024))
    
    delete_from_Json_file("Strom.json", "01.01.2015", "31.12.2015")