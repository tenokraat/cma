import json
import requests
import os


data = {
  'username': 'admin',
  'password': 'Adminhpq-123'
}

r = requests.post('https://cs-aruba-mm.hpearubademo.com:4343/v1/api/login', data=data, verify=False)

r.raw


#def login_os(data, url):
#    username = data['user']
#    password = data['password']
#    params = {'userName': username, 'password': password}
#    proxies = {'http': None, 'https': None}
#    url_login = url + "login-sessions"
#    response = requests.post(url_login, verify=False, data=json.dumps(params), proxies=proxies, timeout=3)
#    if response.status_code == 201:
#        print("Login to switch: {} is successful".format(url_login))
#        session = response.json()
#        r_cookie = session['cookie']
#        return r_cookie
#    else:
#        print("Login to switch failed")