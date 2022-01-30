from urllib3 import PoolManager
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
import requests


HTTP = PoolManager()
HEADERS =   {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }

#This function is used when there is a login page, to get the cookies send in the request 
def connexion_post(response, username, password, base_url):
    scrapper = BeautifulSoup(response.data, features="lxml")    
    formulaire = scrapper.find_all("form")
    form = formulaire[0]
    payload = {}
    inputs = form.find_all("input")
    for i in inputs:
        if i["name"] == "username":
            payload["username"] = username
        elif i["name"] == "password":
            payload["password"] = password
        else :
            payload[i["name"]] = i["value"]
    cookie = SimpleCookie()
    cookie.load(response.getheader("Set-Cookie"))
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    r = requests.post(base_url, payload, cookies = cookies)
    if "Login failed" in r.text:
        print("Login failed")
        pass
    else:
        return cookies

#This function is used to get all the forms of the page we want to scan
def get_forms(url, cookie):
    soup = BeautifulSoup(requests.get(url, headers = HEADERS, cookies = cookie).content, "html.parser")
    return soup.find_all("form") 

#This function is used to get the details of a form
def get_form_details(forms):
    details = {}
    for form in forms :
        try:
            action = form.attrs.get("action").lower()
        except:
            action = None
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
    return details

#This fucntion return True if the url is vulnerable to sql injection
def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower() or response.status_code >= 500:
            return True
    return False

#This function is used to send an incomplete sql request in the input of a form in order to determine if it is vulnerable to sql injection
def scan_sql_injection(url, cookie):
    status = 0
    forms = get_forms(url, cookie)
    print(f"{len(forms)} forms detected on {url}.")
    form_details = get_form_details(forms)
    for c in "\"'":
        data = {}
        for input_tag in form_details["inputs"]:
            if input_tag["type"] == "hidden" or input_tag["value"]:
                try:
                    data[input_tag["name"]] = input_tag["value"] + c
                except:
                    pass
            elif input_tag["type"] != "submit":
                data[input_tag["name"]] = f"test{c}"
        url = urljoin(url, form_details["action"])
        if form_details["method"] == "post":
            res = requests.post(url,headers=HEADERS, data=data, cookies=cookie)
        elif form_details["method"] == "get":
            res = requests.get(url,headers=HEADERS, params=data, cookies=cookie)
        if is_vulnerable(res):
            status = 1
            vulnerable_form = form_details
            break
    if status == 1:
        print(f"One SQL injection vulnerability is detected for the form {vulnerable_form}")
    else:
        print("No SQL Injection vulnerability detected")

def main(target_test_url): 
    response = HTTP.request('GET', target_test_url, None, HEADERS)
    if response.status == 200:
        pass
    try:
        redirect_url = response.retries.history[-1].redirect_location
        if 'login' in redirect_url:
            print()
            answer = input("Do you need to login ? [Y/n] : ")
            if answer == 'Y' or answer == '':
                username = input("Please fill the username : ")
                password = input("Please fill the password : ")
                cookie = connexion_post(response, username, password, target_test_url)
                scan_sql_injection(target_test_url, cookie)
            else:
                answer = input("Do you want to try SQL injection on this page ? [Y/n] : ")
                if answer == 'Y' or answer == '':
                    scan_sql_injection(target_test_url, cookie='')
        else: 
            scan_sql_injection(redirect_url, cookie='')
    except:
        scan_sql_injection(target_test_url, cookie)