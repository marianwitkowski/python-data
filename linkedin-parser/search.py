import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse
from urllib.parse import quote

# wyszukiwana fraza
QS = "programista python"

raw_headers = """
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0
"""

headers = {}
for items in raw_headers.split("\n"):
    if len(items.strip()):
        key, value = items.strip().split(": ")
        headers[key.strip()] = value.strip()


def googleSearch(query):
    counter = 0
    g_clean = []
    url = 'https://www.google.pl/search?q={0}'.format(query)
    try:

        while True:
            html = requests.get(url, headers=headers)
            print(url)
            if html.status_code >= 400:
                print(f"invalid response - {html.status_code}")
                time.sleep(30)
                continue

            if html.status_code == 200:
                soup = BeautifulSoup(html.text, 'lxml')
                counter += 1
                with open(f"log-{counter:04d}.html", "wt") as fd:
                    fd.write(html.text)
                a = soup.find_all('a')
                for i in a:
                    k = i.get('href')
                    try:
                        m = re.search("(?P<url>https?://[^\s]+)", k)
                        n = m.group(0)
                        rul = n.split('&')[0]
                        domain = urlparse(rul)
                        if (re.search('google.', domain.netloc)):
                            continue
                        else:
                            title = i.find('h3')
                            if title:
                                title = title.text.strip()
                            else:
                                title = "---"
                            g_clean.append({"title": str(title), "link": str(rul)})
                    except:
                        continue
                next_link = soup.find("a", attrs={'id': 'pnnext'})
                if next_link:
                    url = next_link.attrs["href"]
                    url = "https://www.google.pl" + url
                    print(f"waiting.....{counter}")
                    time.sleep(5)
                else:
                    break

    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean


QS = f'site:linkedin.com/in "{QS}"'
result = googleSearch(quote(QS))
result = [r.get("title") + "\t\t" + r.get("link") + "\r\n" for r in result]
with open("result.csv", "wt") as fd:
    fd.writelines(result)
