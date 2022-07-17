import requests
import bs4
import re
from datetime import datetime

cities = [
    ('Warszawa','warszawa'),
    ('Poznań', 'poznan'),
    ('Kraków','krakow'),
    ('Łódź', 'lodz'),
    ('Wrocław', 'wroclaw'),
    ('Gdańsk', 'gdansk'),
    ('Szczecin', 'szczecin'),
    ('Bydgoszcz', 'bydgoszcz'),
    ('Lublin', 'lublin'),
    ('Białystok', 'bialystok'),
    ('Katowice', 'katowice'),
    ('Gdynia', 'gdynia'),
    ('Częstochowa', 'czestochowa'),
    ('Radom', 'radom'),
    ('Rzeszów', 'rzeszow'),
    ('Toruń', 'torun'),
    ('Sosnowiec', 'sosnowiec'),
    ('Kielce', 'kielce'),
    ('Gliwice', 'gliwice'),
    ('Olsztyn', 'olsztyn'),
]

def get_data(city):
    cookies = {
        'laquesisff': 'gre-12226#rer-165#rer-166#rst-73#rst-74',
        'OptanonAlertBoxClosed': '2022-05-29T20:07:59.308Z',
        'eupubconsent-v2': 'CPZuhHAPZuhHAAcABBENCRCsAP_AAH_AAAYgIxtf_X__b3_j-_5_f_t0eY1P9_7__-0zjhfdt-8N3f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7_____7z_v-v_v____f_7-3f3__5_3_--_e_V_99zbn9_____9nP___9v-_9_________4IwAEmGpeQBdmWODJtGEUKIEYVhIdQKACigGFoisIHVwU7K4CfUELABAKkJwIgQYgowYBAAIJAEhEQEgB4IBEARAIAAQAKgEIACNgEFgBYGAQACgGhYgRQBCBIQZEBEcpgQFSJRQT2ViCUHexphCHWeAFAo_oqEBGskYLAyEhYOY4AkBLxZIHmKF8gBGCFAAAAA.f_gAD_gAAAAA',
        'OTAdditionalConsentString': '1~89.2008.2072.2322.2465.2501.2999.3028.3225.3226.3231.3232.3234.3235.3236.3237.3238.3240.3241.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3293.3295.3296.3300.3305.3308',
        'ldTd': 'true',
        '_gcl_au': '1.1.285671664.1653854880',
        '__gfp_64b': 'neeLLOvDm72f3H7pHgt_q9Fy1e3UBDtprn0AmnGwGTb.g7|1653854879',
        'PHPSESSID': 'has5o3o5fd4tela3h0fn8gdhev',
        'mobile_default': 'desktop',
        'ninja_user_status': 'unlogged',
        'observed5_id_clipboard': '6293d2a8dcbe6',
        'observed5_sec_clipboard': 'PYhUGw2Zut2YiJiu27Dgrpf6lAS6a5Z5',
        'laquesissu': '294@survey_answer|1#315@my_account|0',
        'laquesis': 'rema-12@b#remt-124@c#smr-361@a',
        '_gid': 'GA1.2.590368974.1653991008',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+May+31+2022+12%3A07%3A53+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=6.32.0&isIABGlobal=false&hosts=&genVendors=V9%3A0%2C&consentId=19e05287-d92f-4ea6-83c0-c4f2072be17a&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2Cgad%3A1%2CSTACK42%3A1&geolocation=PL%3B14&AwaitingReconsent=false',
        '_gat_clientNinja': '1',
        '_ga': 'GA1.2.283861361.1653854879',
        '_gat_UA-124076552-11': '1',
        'onap': '181116eabb7x91e5b64-4-181198be584x757b40fb-236-1653995255',
        '_ga_HL51DW3Q97': 'GS1.1.1653991003.2.1.1653993455.60',
        'lqstatus': '1653994676|181198be584x757b40fb|rema-12#smr-361||',
    }

    headers = {
        'authority': 'www.otodom.pl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'laquesisff=gre-12226#rer-165#rer-166#rst-73#rst-74; OptanonAlertBoxClosed=2022-05-29T20:07:59.308Z; eupubconsent-v2=CPZuhHAPZuhHAAcABBENCRCsAP_AAH_AAAYgIxtf_X__b3_j-_5_f_t0eY1P9_7__-0zjhfdt-8N3f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7_____7z_v-v_v____f_7-3f3__5_3_--_e_V_99zbn9_____9nP___9v-_9_________4IwAEmGpeQBdmWODJtGEUKIEYVhIdQKACigGFoisIHVwU7K4CfUELABAKkJwIgQYgowYBAAIJAEhEQEgB4IBEARAIAAQAKgEIACNgEFgBYGAQACgGhYgRQBCBIQZEBEcpgQFSJRQT2ViCUHexphCHWeAFAo_oqEBGskYLAyEhYOY4AkBLxZIHmKF8gBGCFAAAAA.f_gAD_gAAAAA; OTAdditionalConsentString=1~89.2008.2072.2322.2465.2501.2999.3028.3225.3226.3231.3232.3234.3235.3236.3237.3238.3240.3241.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3293.3295.3296.3300.3305.3308; ldTd=true; _gcl_au=1.1.285671664.1653854880; __gfp_64b=neeLLOvDm72f3H7pHgt_q9Fy1e3UBDtprn0AmnGwGTb.g7|1653854879; PHPSESSID=has5o3o5fd4tela3h0fn8gdhev; mobile_default=desktop; ninja_user_status=unlogged; observed5_id_clipboard=6293d2a8dcbe6; observed5_sec_clipboard=PYhUGw2Zut2YiJiu27Dgrpf6lAS6a5Z5; laquesissu=294@survey_answer|1#315@my_account|0; laquesis=rema-12@b#remt-124@c#smr-361@a; _gid=GA1.2.590368974.1653991008; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+31+2022+12%3A07%3A53+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=6.32.0&isIABGlobal=false&hosts=&genVendors=V9%3A0%2C&consentId=19e05287-d92f-4ea6-83c0-c4f2072be17a&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2Cgad%3A1%2CSTACK42%3A1&geolocation=PL%3B14&AwaitingReconsent=false; _gat_clientNinja=1; _ga=GA1.2.283861361.1653854879; _gat_UA-124076552-11=1; onap=181116eabb7x91e5b64-4-181198be584x757b40fb-236-1653995255; _ga_HL51DW3Q97=GS1.1.1653991003.2.1.1653993455.60; lqstatus=1653994676|181198be584x757b40fb|rema-12#smr-361||',
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    }

    params = {
        'distanceRadius': '5',
        'page': '1',
        'limit': '36',
        'market': 'ALL',
    }

    try:
        url = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{city}'
        response = requests.get(url,
                                params=params, cookies=cookies, headers=headers)

        if response.status_code:
            return response.text
        return None
    except Exception as exc:
        return None

ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for city in cities:
    data = get_data(city[1])
    if data:
        dom = bs4.BeautifulSoup( data, "lxml")
        tags = dom.find_all("meta")
        if tags:
            for tag in tags:
                if "description"in tag.attrs.values():
                    s = tag.get("content")
                    res = re.findall(r'\b\d+\b', s)
                    if len(res)>0:
                        print("OTODOM",ts,city[0],res[0], sep="|")
                        continue



