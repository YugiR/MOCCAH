import socket
import requests
import pprint
import json
import requests
import phonenumbers
import folium
import sys
import pyfiglet
from datetime import datetime
from phonenumbers import geocoder
from bs4 import BeautifulSoup
from urllib.parse import urljoin


ascii_banner = pyfiglet.figlet_format("MOCCAH")
print(ascii_banner)
print("Created by @Yugi")
print("Menu hacking: ")
print("1. Information Gathering Pasif")
print("2. scanning XSS Vulnerability")
print("3. SQL injection scanner")
print("4. SubDomain Scanner")
print("5. Track Location number")
print("6. Port Scanner")
pilih = int(input('which one do you want??? '))

match pilih:
        case 1:
                #mencari alamat dari domain
                print ("example : example.com")
                host = input('Enter a domain name: ')
                ip_address = socket.gethostbyname(host)
                url = 'https://geolocation-db.com/jsonp/' + ip_address
                response = requests.get(url)
                geolocation = response.content.decode()
                geolocation = geolocation.split("(")[1].strip(")")
                geolocation = json.loads(geolocation)
                for k,v in geolocation.items():
                        pprint.pprint(str(k) + ' : ' + str(v))
                
        case 2: 
                #scanning xss
                print ("example : https://example.com/")
                target = input("Enter a domain name : ")

                payload = "<script>alert(xss);</script>"
                req = requests.post(target + payload)

                if payload in req.text:
                        print ("XSS Vulnerability Founds!!!")
                        print ("Attack payload: " + payload)
                else:
                        print("Domain Secure")
        case 3:
                print("example: https://example.com/")
                domain = input("Enter a domain name : ")
                s = requests.Session()
                s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
                def get_forms(url):
                        soup = BeautifulSoup(s.get(url).content, "html.parser")
                        return soup.find_all("form")
                def form_details(form):
                        detailsOfForm = {}
                        action = form.attrs.get("action")
                        method = form.attrs.get("method", "get")
                        inputs = []
                        for input_tag in form.find_all("input"):
                            input_type = input_tag.attrs.get("type", "text")
                            input_name = input_tag.attrs.get("name")
                            input_value = input_tag.attrs.get("value", "")
                            inputs.append({
                                "type": input_type, 
                                "name" : input_name,
                                "value" : input_value,
                             })
                        detailsOfForm['action'] = action
                        detailsOfForm['method'] = method
                        detailsOfForm['inputs'] = inputs
                        return detailsOfForm
                def vulnerable(response):
                        errors = {"The quoted string is not terminated properly", 
                                  "Unclosed quotes after a character string",
                                  "There is an error in your sqlinjection syntax" 
                                 }
                        for error in errors:
                            if error in response.content.decode().lower():
                                return True
                        return False
                def sql_injection_scan(url):
                        forms = get_forms(url)
                        print(f"Founds {len(forms)} In URL {url}.")
                        for form in forms:
                                details = form_details(form)
                                for i in "\"'":
                                        data = {}
                                        for input_tag in details["inputs"]:
                                              if input_tag["type"] == "hidden" or input_tag["value"]:
                                                data[input_tag['name']] = input_tag["value"] + i
                                              elif input_tag["type"] != "submit":
                                                data[input_tag['name']] = f"test{i}"
                                        print(url)
                                        form_details(form)
                                        if details["method"] == "post":
                                                res = s.post(url, data=data)
                                        elif details["method"] == "get":
                                                res = s.get(url, params=data)
                                        if vulnerable(res):
                                                print("SQL injection its Found!! ", url )
                                        else:
                                                print("Domain secure")
                                                break
                if __name__ == "__main__":
                        urlToBeChecked = domain
                        sql_injection_scan(urlToBeChecked)     
        case 4:
                print("example : example.com")
                urlDomain = input("Enter a domain name : ")
                def find_subdomain(domain, timeout=3):
                        wordlist = [
                                "admin",
                                "api",
                                "blog",
                                "chat",
                                "image",
                                "portal",
                                "elearning",
                                "login",
                                "mail",
                                "wp-admin"
                        ]
                        
                        for subdomain in wordlist:
                                urlT = f"http://{subdomain}.{domain}"
                                try:
                                        response = requests.get(urlT)
                                        status = response.status_code
                                        print(f"{urlT} - {status}")
                                except requests.exceptions.RequestException:
                                        timeout
                                        pass
                                urlT = f"https://{subdomain}.{domain}"
                                try:
                                        response = requests.get(urlT)
                                        status = response.status_code
                                        print(f"{urlT} - {status}")
                                except requests.exceptions.RequestException:
                                        timeout
                                        pass
                domain = urlDomain
                timeout = 4
                find_subdomain(domain, timeout)
        case 5:
                print("example : +1234567890")
                number = input("Enter number : ")
                pepnumber = phonenumbers.parse(number)
                location = geocoder.description_for_number(pepnumber, "en")
                print(location)
                
                from phonenumbers import carrier
                service_pro = phonenumbers.parse(number)
                print(carrier.name_for_number(service_pro, "en"))

                from opencage.geocoder import OpenCageGeocode
                key = 'a92be551ba454746ae3f6166faa6f722'

                geocoder = OpenCageGeocode(key)
                query = str(location)
                results = geocoder.geocode(query)
                lat = results[0]['geometry']['lat']
                lng = results[0]['geometry']['lng']

                print(lat, lng)

                myMap = folium.Map(location=[lat, lng], zoom_start=9)
                folium.Marker([lat, lng], popup=location).add_to(myMap)
                
        case 6 :
                print("example : 123.456.789")
                target = input(str("Target IP : "))
                print("_" * 50)
                print("scanning Target: " + target)
                print("scanning started at: " + str(datetime.now()))
                print("_" * 50)
                
                try:
                        for port in range(1,65535):
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                socket.setdefaulttimeout(0.5)
        
                                result = s.connect_ex((target,port))
                                if result == 0:
                                        print("[*] Port {} terbuka".format(port))
                                        s.close()
                except KeyboardInterrupt:
                        print("\n Keluar : (")
                        sys.exit()
                except socket.error:
                        print("\ Host tidak terhubung :(")
                        sys.exit()
