"""
Script module, just a console wrapper for the insecam.org handles,
works with vanilla python3, tested with Python 3.11.2 and pypy3
github.com/AngelSecurityTeam/Cam-Hackers
github.com/YarBurArt/Cam-API-Enhanced
"""
#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import re
import urllib.request
import urllib.error
import json


def get_data(url):
    """ obtain data for analysis purposes """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.insecam.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8')

def save_ips_to_file(country_f, ips):
    """ archive IP addresses for record-keeping """
    with open(f'{country_f}.txt', 'w', encoding="utf-8") as f:
        for ip in ips:
            print("\n\033[1;31m", ip)
            f.write(f'{ip}\n')

BASE_URL = "http://www.insecam.org/en/jsoncountries/"
BYCOUNTRY_URL = "http://www.insecam.org/en/bycountry/"

rsp = get_data(BASE_URL)
data = json.loads(rsp)
countries = data['countries']

print("""
\033[1;31m\033[1;37m ██████╗ █████╗ ███╗   ███╗      ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ███████╗
██╔════╝██╔══██╗████╗ ████║      ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝
██║     ███████║██╔████╔██║█████╗███████║███████║██║     █████╔╝ █████╗  ██████╔╝███████╗
██║     ██╔══██║██║╚██╔╝██║╚════╝██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗╚════██║
╚██████╗██║  ██║██║ ╚═╝ ██║      ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║███████║
\033[1;31m ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
\033[1;31m                                                                        ANGELSECURITYTEAM \033[1;31m\033[1;37m""")

for key, value in countries.items():
    print(f'Code : ({key}) - {value["country"]} / ({value["count"]})  \n')

try:
    country = input("Code(##) : ")
    res = get_data(f"{BYCOUNTRY_URL}{country}")
    last_page = re.findall(
        r'pagenavigator\("\?page=", (\d+)', res.text)[0]

    for page in range(int(last_page)):
        res = get_data(f"{BYCOUNTRY_URL}{country}/?page={page}")
        find_ip = re.findall(r"http://\d+.\d+.\d+.\d+:\d+", res.text)

        save_ips_to_file(country, find_ip)

except urllib.error.URLError as e:
    print(f"Error accessing URL: {e}")
    sys.exit(1)
except UnicodeDecodeError as e:
    print(f"Error decoding data: {e}")
    sys.exit(1)

finally:
    print("\033[1;37m")
    print('\033[37mSave File :'+country+'.txt')
    sys.exit(0)
