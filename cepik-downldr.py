import requests
import json
import pandas as pd
import re
from func import *


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
        break
    else:
        print("Podałeś niewłaściwą opcję!!!! Spróbuj jeszcze raz!")


pojazdy = cepik_download(date01, date02, voivodship, choice)

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
print("\n1. Całe zestawienie pojazdów")
print("2. Pojazdy wybrane wg moich kryteriów")
reporting = input("Wybierz opcję 1 lub 2: ")


######### Exporting File ####################

if reporting == "1":
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    pojazdy.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "2":
    print("Odpowiedz na pytania dotyczące tego, co ma się znaleźć w zestawieniu pojazdów")
    if export_option("Czy ująć w zestawieniu samochody osobowe") == True:
        exported_data = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD OSOBOWY")]
    else:
        exported_data = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD OSOBOWY")]

    if export_option("Czy ująć w zestawieniu samochody ciężarowe") == True:
         trucks = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD CIĘŻAROWY")]
         exported_data = pd.concat([trucks, exported_data], ignore_index=True)
    else:
        pass

    if export_option("Czy ująć w zestawieniu samochody motocykle") == True:
         bikes = pojazdy[(pojazdy.rodzaj == "MOTOCYKL")]
         exported_data = pd.concat([bikes, exported_data], ignore_index=True)
    else:
        pass

    if export_option("Czy ująć w zestawieniu ciągniki rolnicze?") == True:
         tracktors = pojazdy[(pojazdy.rodzaj == "CIĄGNIK ROLNICZY")]
         exported_data = pd.concat([tracktors, exported_data], ignore_index=True)
    else:
        pass

    if export_option("Czy ująć w zestawieniu naczepy i przyczepy?") == True:
         trailers = pojazdy[(pojazdy.rodzaj == "NACZEPA CIĘŻAROWA") + (pojazdy.rodzaj == "PRZYCZEPA CIĘŻAROWA") + (pojazdy.rodzaj == "PRZYCZEPA LEKKA")]
         exported_data = pd.concat([trailers, exported_data], ignore_index=True)
    else:
        pass

    if export_option("Czy ująć w zestawieniu tylko pojazdy danych marek?") == True:
         brands = input("Podaj interesującą Cię markę lub marki. Jeśli podajesz więcej niż jedną, oddziel je przecinkami: ")
         brands = brands.upper()
         brands = brands.replace(" ", "")
         brands = brands.split(",")
         exported_data_brands = exported_data[(exported_data.marka == "")]
         for brand in brands:
              cars__given_brand = exported_data[(exported_data.marka == brand)]
              exported_data_brands = pd.concat([cars__given_brand, exported_data_brands], ignore_index=True)

         exported_data = exported_data_brands
    else:
        pass

    pojazdy["nowe"] = pojazdy.pochodzenie.apply(lambda x: True if "NOWY" in x else False)
    pojazdy["import"] = pojazdy.pochodzenie.apply(lambda x: True if "IMPORT" in x else False)

    if export_option("Czy uwzględnić w zestawieniu pojazdy nowe") == True:
        exported_data = pojazdy[pojazdy.nowe == True]
    else:
        pass

    if export_option("Czy uwzględnić w zestawieniu tylko pojazdy używane lub zakupione po przepadku na rzecz skarbu państwa?") == True:
        exported_data = pojazdy[pojazdy.nowe == False]
    else:
        pass

    if export_option("Czy uwzględnić w zestawieniu tylko pojazdy importowane?") == True:
        exported_data = pojazdy[pojazdy.import == True]
    else:
        pass


    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    exported_data.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))


"""


    trailers = pojazdy[(pojazdy.rodzaj == "NACZEPA CIĘŻAROWA") + (pojazdy.rodzaj == "PRZYCZEPA CIĘŻAROWA") + (pojazdy.rodzaj == "PRZYCZEPA LEKKA")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    trailers.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))
elif reporting == "8":
    new_cars = pojazdy[(pojazdy.pochodzenie == "NOWY ZAKUPIONY W KRAJU")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    new_cars.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))

# poprawić import nowych i używanych

elif reporting == "9":
    new_cars = pojazdy[(pojazdy.pochodzenie == "UŻYW. ZAKUPIONY W KRAJU")]
    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    new_cars.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))

##########33
#############333
####################3

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
        exported_data = pojazdy[(pojazdy.rodzaj == "SAMOCHÓD OSOBOWY")]

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

    while True:
        bikes_yes_or_no = input("Czy ująć w zestawieniu samochody motocykle (t/n): ")
        if bikes_yes_or_no == "n" or trucks_yes_or_no == "N":
            bikes_yes_or_no = False
            break
        elif bikes_yes_or_no == "t" or bikes_yes_or_no == "T":
            bikes_yes_or_no = True
            break
        else:
            print("Nie ma takiej opcji!!!")
            continue

    if bikes_yes_or_no == True:
         bikes = pojazdy[(pojazdy.rodzaj == "MOTOCYKL")]
         exported_data = pd.concat([bikes, exported_data], ignore_index=True)

    while True:
        tracktors_yes_or_no = input("Czy ująć w zestawieniu samochody ciągniki rolnicze? (t/n): ")
        if tracktors_yes_or_no == "n" or tracktors_yes_or_no == "N":
            bikes_tracktors_yes_or_noyes_or_no = False
            break
        elif tracktors_yes_or_no == "t" or tracktors_yes_or_no == "T":
            tracktors_yes_or_no = True
            break
        else:
            print("Nie ma takiej opcji!!!")
            continue

    if tracktors_yes_or_no == True:
        tracktors = pojazdy[(pojazdy.rodzaj == "CIĄGNIK ROLNICZY")]
        exported_data = pd.concat([tracktors, exported_data], ignore_index=True)

    exported_data.to_csv('testowy2.csv', index=False)

    while True:
        trailers_yes_or_no = input("Czy ująć w zestawieniu przyczepy i naczepy? (t/n): ")
        if trailers_yes_or_no == "n" or trailers_yes_or_no == "N":
            trailers_yes_or_no = False
            break
        elif trailers_yes_or_no == "t" or trailers_yes_or_no == "T":
            trailers_yes_or_no = True
            break
        else:
            print("Nie ma takiej opcji!!!")
            continue

    if trailers_yes_or_no == True:
        trailers = pojazdy[(pojazdy.rodzaj == "NACZEPA CIĘŻAROWA") + (pojazdy.rodzaj == "PRZYCZEPA CIĘŻAROWA") + (pojazdy.rodzaj == "PRZYCZEPA LEKKA")]
        exported_data = pd.concat([tracktors, exported_data], ignore_index=True)

    ################# Dokończyć eksport wg wielu kryteriów


    nazwa_pliku = input("Podaj nazwę pliku, do którego chcesz zapisać dane: ")
    nazwa_pliku = nazwa_pliku + ".csv"
    exported_data.to_csv(nazwa_pliku, index=False)
    print("Pomyślnie wyeksportowano plik {}".format(nazwa_pliku))

else:
    print("Błąd! Funkcja jeszcze nie zaimplementowana")

"""
