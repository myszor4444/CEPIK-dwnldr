import requests
import json
import pandas as pd
import re


######### DATA REQUEST ####################

print("Witaj w programie CEPIK Searcher, który pobiera dane z CEPIK :)")


while True:
    date01 = input("Podaj datę początkową w formacie RRRRMMDD: ")
    match_check = re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", date01)
    if bool(match_check) == True:
        break
    else:
        print("ZŁY FORMAT DATY! Podaj datę początkową w formacie RRRRMMDD: ")
        continue

while True:
    date02 = input("Podaj datę końcową w formacie RRRRMMDD: ")
    match_check = re.fullmatch("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", date02)
    if bool(match_check) == True:
        break
    else:
        print("ZŁY FORMAT DATY! Podaj datę końcową w formacie RRRRMMDD: ")
        continue

print("""
Kody TERYT województw:
dolnośląskie - 02,
kujawsko-pomorskie - 04,
lubelskie - 06,
lubuskie - 08,
łódzkie - 10,
małopolskie - 12,
mazowieckie - 14,
opolskie - 16,
podkarpackie - 18,
podlaskie - 20,
pomorskie - 22,
śląskie - 24,
świętokrzyskie - 26,
warmińsko-mazurskie - 28,
wielkopolskie - 30,
zachodniopomorskie - 32.
""")

while True:
    voivodship = input("\nPodaj kod TERYT województwa: ")
    teryt_codes = ["02", "04", "06", "08", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32"]
    if voivodship in teryt_codes:
        break
    else:
        print("NIEPRAWIDŁOWY KOD TERYT! Podaj kod jeszcze raz: ")

while True:
    print("\nJakie dane chcesz zobaczyć?")
    print("1. Dane pojazdów zarejestrowanych po raz pierwszy w przedziale dat")
    print("2. Dane pojazdów, których data ostatniej rejestracji mieści się w przedziale dat.")

    choice = input("Wybierz opcję 1 lub 2: ")

    if choice == "1":
        cepik_url = "https://api.cepik.gov.pl/pojazdy?wojewodztwo=" + voivodship + "&data-od=" + date01 + "&data-do=" + date02
        break
    elif choice == "2":
        cepik_url = "https://api.cepik.gov.pl/pojazdy?wojewodztwo=" + voivodship + "&data-od=" + date01 + "&data-do=" + date02 + "&typ-daty=2"
        break
    else:
        print("Podałeś niewłaściwą opcję!!!! Spróbuj jeszcze raz!")


print("\nPobieram dane z CEPIK....")
pojazdy_request = requests.get(cepik_url)

print("\nPrzetwarzam dane...")
dicction = json.loads(pojazdy_request.text)
dicction2 = dicction["data"]

pojazdy = pd.DataFrame.from_dict(dicction2)

######### DATA WRANGLING ####################

marki = []

for i in pojazdy.attributes:
    marki.append(i['marka'])

pojazdy['marka'] = marki

modele = []

for i in pojazdy.attributes:
    modele.append(i['model'])

pojazdy['model'] = modele

rodzaje = []

for i in pojazdy.attributes:
    rodzaje.append(i['rodzaj-pojazdu'])

pojazdy['rodzaj'] = rodzaje

daty = []

for i in pojazdy.attributes:
    daty.append(i['data-pierwszej-rejestracji-w-kraju'])

pojazdy['data_pierw_rejestr'] = daty

origins = []

for i in pojazdy.attributes:
    origins.append(i['pochodzenie-pojazdu'])

pojazdy["pochodzenie"] = origins

fuel = []

for i in pojazdy.attributes:
    fuel.append(i['rodzaj-paliwa'])

pojazdy['paliwo'] = fuel

engine = []

for i in pojazdy.attributes:
    engine.append(i['pojemnosc-skokowa-silnika'])

pojazdy['poj_silnika'] = engine

pojazdy.drop('type', inplace=True, axis=1)
pojazdy.drop('attributes', inplace=True, axis=1)

def change(dicto):
    return dicto['self']

pojazdy['links'] = pojazdy.links.apply(change)

############ Exporting Options #################

print("\nJakiego rodzaju dane chcesz wyeksportować?")
print("\n1. Ogólne zestawienie pojazdów")
print("2. Zestawienie pojazdów danej marki")
print("3. Tylko samochody osobowe")
print("4. Tylko motocykle")
print("5. Tylko ciężarówki")
print("6. Tylko ciągniki")
print("7. Tylko przyczepy i naczepy")
print("8. Tylko pojazdy nowe, zakupione w kraju")
print("9. Tylko pojazdy używane, zakupione w kraju")
print("10. Pojazdy wybrane wg kilku kryteriów")
reporting = input("Wybierz opcję od 1 do 9: ")


######### Exporting File ####################

if reporting == "1":
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    pojazdy.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "2":
    brand = input("Podaj markę, która Cię interesuje: ")
    brand = brand.upper()
    cars__given_brand = pojazdy[(pojazdy.marka == brand)]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    cars__given_brand.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "3":
    cars = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD OSOBOWY")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    cars.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "4":
    bikes = pojazdy[(pojazdy.rodzaj == "MOTOCYKL")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    bikes.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "5":
    trucks = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD CIĘŻAROWY")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    trucks.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "6":
    tracktors = pojazdy[(pojazdy.rodzaj == "CIĄGNIK ROLNICZY")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    tracktors.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "8":
    new_cars = pojazdy[(pojazdy.pochodzenie == "NOWY ZAKUPIONY W KRAJU")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    new_cars.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "9":
    new_cars = pojazdy[(pojazdy.pochodzenie == "UŻYW. ZAKUPIONY W KRAJU")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    new_cars.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "10":
    print("Odpowiedz na pytania dotyczące tego, co ma się znaleźć w zestawieniu pojazdów")
    while True:
        personal_yes_or_no = input("Czy ująć w zestawieniu samochody osobowe (t/n): ")
        if personal_yes_or_no == "n" or personal_yes_or_no == "N":
            personal_yes_or_no = False
            break
        elif personal_yes_or_no == "t" or personal_yes_or_no == "T":
            personal_yes_or_no = True
            break
        else:
            print("Nie ma takiej opcji!!!")
            continue

    if personal_yes_or_no == True:
        exported_data = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD OSOBOWY")]
    elif personal_yes_or_no == False:
        exported_data = pd.DataFrame.empty

    while True:
        trucks_yes_or_no = input("Czy ująć w zestawieniu samochody ciężarowe (t/n): ")
        if trucks_yes_or_no == "n" or trucks_yes_or_no == "N":
            trucks_yes_or_no = False
            break
        elif trucks_yes_or_no == "t" or trucks_yes_or_no == "T":
            trucks_yes_or_no = True
            break
        else:
            print("Nie ma takiej opcji!!!")
            continue

    if trucks_yes_or_no == True:
         trucks = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD CIĘŻAROWY")]
         exported_data = pd.concat([trucks, exported_data], ignore_index=True)

    exported_data.to_csv('testowy.csv', index=False)

    #### dokończyć opcję eksportu wielokryteriowego


else:
    print("Błąd! Funkcja jeszcze nie zaimplementowana")
