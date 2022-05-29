import requests

# URL oferty
offer_url = 'https://www.otomoto.pl/oferta/bmw-seria-3-xdrive-salon-pl-adaptive-led-m-pak-pakiet-napraw-bmw-ID6EEGnW.html'

offer_id = offer_url.split("-")[-1].strip(".html")[2:]
print(f"ID oferty: {offer_id}") #ID oferty: 6EEGnW

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Referer': offer_url,
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

response = requests.get(f'https://www.otomoto.pl/ajax/misc/contact/all_phones/{offer_id}/',
                        headers=headers)
print(f"Kontakt: {response.json()}")
# Kontakt: [{'label': '516 930 256', 'number': '516930256'}]