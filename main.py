from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from models import db, User, Region
from time import sleep
import logging
from random import choice
from bs4 import BeautifulSoup
import requests
import json

logging.basicConfig(level=logging.INFO)


class JokerAvcisi:
    def __init__(self):
        self.browser = None
        self.base_url = "https://www.yemeksepeti.com/ankara"
        self.url = "https://www.yemeksepeti.com"
        self.is_authenticated = False
        self.open_connection()
        self.init_database()

    @staticmethod
    def init_database():
        db.create_tables([User, Region])

    @staticmethod
    def open_connection():
        db.connect()

    @staticmethod
    def destroy_connection():
        db.close()

    @staticmethod
    def init_webdriver():
        return webdriver.Chrome(ChromeDriverManager().install())

    def authenticate(self):
        user = User.select().first()
        if user is not None:
            self.browser.get(self.base_url)
            username_input = self.browser.find_element_by_id("UserName")
            username_input.send_keys(user.email)
            password_input = self.browser.find_element_by_id("password")
            password_input.send_keys(user.password)
            self.browser.find_element_by_id("ys-fastlogin-button").click()
            sleep(1)
            try:
                self.browser.find_element_by_id("UserName")
                self.is_authenticated = False
                logging.error('Giriş yapılamadı...')
                self.browser.quit()
            except:
                self.is_authenticated = True
                logging.info('Başarı ile giriş yapıldı...')
        else:
            logging.error(
                'Kullanıcı mevcut değil. '
                'yemeksepeti.db database içerisindeki user '
                'tablosuna yemeksepeti hesabınızı ekleyiniz.')
            self.is_authenticated = False

    def main(self):
        self.browser = self.init_webdriver()
        self.authenticate()
        if self.is_authenticated is True:
            self.loop_regions()

    def check_criteria(self):
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        willcards = soup.select('a.joker-offer-item')
        data = []
        for willcard in willcards:
            restaurant_url = f"{self.url}{willcard.get('data-href')}"
            response = requests.get(restaurant_url)
            if response.status_code == 200:
                _soup = BeautifulSoup(response.content, 'lxml')
                points = _soup.select('span.point')
                point_text = f"Hız: {points[0].text} / Servis: {points[1].text} / Lezzet: {points[2].text}"
                scripts = _soup.select('script[type="application/ld+json"]')
                _json = None
                for script in scripts:
                    _json = json.loads(script.string)

                    if 'paymentAccepted' in _json:
                        if 'Ticket Restaurant Yemek Kartı' in _json['paymentAccepted']:
                            _json['status'] = True
                        else:
                            _json['status'] = False
                        _json['points'] = point_text
                        data.append(_json)
        return data

    def loop_regions(self):
        regions = Region.select()
        if len(regions) > 0:
            while True:
                try:
                    region = choice(regions)
                    logging.info(f"{region.region_name} joker aranıyor...")
                    self.browser.get(region.region_url)
                    sleep(3)
                    wildcard_logo = self.browser.find_element_by_class_name("jokerLogo")
                    if wildcard_logo is not None:
                        logging.info(f"{region.region_name} joker bulundu!\n")
                        sleep(0.2)
                        criteria_data = self.check_criteria()

                        for data in criteria_data:
                            if data['status'] is True:
                                text = f"\nRestorant Adı: {data['name']}\n" \
                                       f"Ödeme Şekli: Ticket Restaurant Yemek Kartı geçerlidir.\n" \
                                       f"Adres:{data['address']['addressLocality']}\n" \
                                       f"{data['points']}\n"
                            else:
                                text = f"\nRestorant Adı: {data['name']}\n" \
                                       f"Ödeme Şekli: Ticket Restaurant Yemek Kartı geçerli değildir.\n" \
                                       f"Adres:{data['address']['addressLocality']}\n" \
                                       f"{data['points']}\n"
                            logging.info(text)
                        sleep(2)
                        status = input("Geçmek istiyor musunuz? e/h: ")
                        if status == 'e':
                            self.browser.find_element_by_id("cboxClose").click()
                            sleep(0.5)
                            continue
                        else:
                            logging.info('Jokeri seçebilmeniz için 17 dakika bekleniyor...')
                            sleep(17 * 60)
                except:
                    logging.error(f"{region.region_name} joker bulunamadı geçiliyor...")
        else:
            logging.error("Region tablosunda kayıt mevcut değil!"
                          "Önce yemeksepetinde gezmesini istediğiniz semtleri region tablosuna ekleyiniz.")
            self.browser.quit()


if __name__ == '__main__':
    ja = JokerAvcisi()
    ja.main()
    # ja.check_criteria()
