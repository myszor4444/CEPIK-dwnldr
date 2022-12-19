
import requests
import pandas as pd
import json

def cepik_download(date01, date02, voivodship, date_type):
    if date_type == 1:
        cepik_url = "https://api.cepik.gov.pl/pojazdy?wojewodztwo=" + voivodship + "&data-od=" + date01 + "&data-do=" + date02
    else:
        cepik_url = "https://api.cepik.gov.pl/pojazdy?wojewodztwo=" + voivodship + "&data-od=" + date01 + "&data-do=" + date02 + "&typ-daty=2"

    print("\nPobieram dane z CEPIK....")
    pojazdy_request = requests.get(cepik_url)

    print("\nPrzetwarzam dane...")
    dicction = json.loads(pojazdy_request.text)
    dicction2 = dicction["data"]

    pojazdy = pd.DataFrame.from_dict(dicction2)

    return pojazdy
