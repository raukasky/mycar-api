from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sqlite3
from sqlite3 import Error


URL = 'https://mycar.kz/cars'

CARS_CLASS = 'css-1twrlxf-CarResultCardData'
CAR_MODEL_CLASS = 'css-333m90-Typography-interSemiBold-sub1'
CAR_PRICE_CLASS = 'css-1uqeuzh-H5-interRegular-bold32'
CAR_YEAR_CLASS = 'css-1ndogut-Typography-interSemiBold-sub1'
CAR_MILEAGE_CLASS = 'css-mmm1cf-Typography-interRegular-pRegular12'


def create_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def insert_data(conn, value):
    sql = '''INSERT INTO CARS_API_CAR(model, price, year, mileage) VALUES (?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()
    return cur.lastrowid


def parse_text(txt):
    return ''.join(filter(lambda i: i.isdigit(), txt))


def scrapping_site(url):
    database = r"./db.sqlite3"
    conn = create_connect(database)
    # Selenium Start
    browser = webdriver.Chrome("./chromedriver")
    browser.get(url)
    browser.find_element_by_xpath("//button[contains(., 'Принять')]").click()
    n = 10
    for i in range(1, n):
        browser.find_element_by_xpath("//button[contains(., 'Загрузить ещё')]").click()
        i += 1
    time.sleep(10)

    # BS4 Start
    try:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        cars = soup.findAll('div', {'class': CARS_CLASS})
        for car in cars:
            car_model = car.find('span', {'class': CAR_MODEL_CLASS}).text
            car_price = car.find('h4', {'class': CAR_PRICE_CLASS}).text
            car_year = car.find('span', {'class': CAR_YEAR_CLASS}).text
            car_mileage = car.find('span', {'class': CAR_MILEAGE_CLASS}).text

            with conn:
                value = (car_model, parse_text(car_price),
                         car_year, (parse_text(car_mileage) if parse_text(car_mileage) is not '' else '0'))
                insert_data(conn, value)

    except Exception as e:
        print('Не удалось распарсить страницу')
        print(e)
    browser.quit()


if __name__ == '__main__':
    scrapping_site(url=URL)
