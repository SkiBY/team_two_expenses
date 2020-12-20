import requests
from lxml import etree
from bs4 import BeautifulSoup

def rate():

    course = ['USD', 'EU', 'RUB', 'BYN']
    response = requests.get('http://www.ecopress.by/ru/sect/61.html')
    soup = BeautifulSoup(response.text, features='lxml')
    money = soup.find_all('th', {'class': 'best'})

    all_courses = []
    for i in money:
        if i.text != '-':
            all_courses.append(float(i.text))

    exchange_rates = {'BYN': 1}
    k = 1
    for i in range(len(course) - 1):
        exchange_rates[course[i]] = all_courses[k]
        k += 2
    exchange_rates['RUB'] = exchange_rates['RUB'] * 0.01
    return exchange_rates

