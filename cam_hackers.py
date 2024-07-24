#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# github.com/AngelSecurityTeam/Cam-Hackers
import sys
import re
import urllib.request
import json

def get_data(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8')

def save_ips_to_file(country, ips):
    with open(f'{country}.txt', 'w', encoding="utf-8") as f:
        for ip in ips:
            print("\n\033[1;31m", ip)
            f.write(f'{ip}\n')

BASE_URL = "http://www.insecam.org/en/jsoncountries/"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.insecam.org",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

rsp = get_data(BASE_URL, headers)
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
    res = get_data(f"http://www.insecam.org/en/bycountry/{country}", headers=headers)
    last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)[0]

    for page in range(int(last_page)):
        res = get_data(f"http://www.insecam.org/en/bycountry/{country}/?page={page}", headers=headers)
        find_ip = re.findall(r"http://\d+.\d+.\d+.\d+:\d+", res.text)

        save_ips_to_file(country, find_ip)
except:
    print("Something went wrong and now you have to deal with it, try python -v cam_hackers.py :)")
    sys.exit(1)

finally:
    print("\033[1;37m")
    print('\033[37mSave File :'+country+'.txt')

    sys.exit(0)
