import requests
from bs4 import BeautifulSoup
import time
import smtplib

class Currency:
    DOLLAR_TG = 'https://mig.kz/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price())

    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_TG, headers=self.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("td", {"class": "sell"})
        return convert[0].text

    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            print('Курс сильно вырос')
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print('Курс сильно упал')
            self.send_mail()
        print('Сейчас курс 1 доллара = ' + str(currency))
        time.sleep(5)
        self.check_currency()

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('MAIL', 'PASSWORD')

        subject = 'Currency mail'
        body = 'Currency has been changed!'
        message = 'Subject: {}\n{}'.format(subject, body)

        server.sendmail(
            'От кого',
            'Кому',
            message
        )
        server.quit()

currency = Currency()
currency.check_currency()