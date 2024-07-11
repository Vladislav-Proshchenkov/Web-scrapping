import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def wait_element(browser, delay_seconds=1, by=By.CLASS_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )

path = ChromeDriverManager().install()
browser_service = Service(executable_path=path)
browser = Chrome(service=browser_service)

browser.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
list_of_vacancies_tag = browser.find_element(By.CLASS_NAME, "vacancy-serp-content")
list_of_vac_tag = list_of_vacancies_tag.find_elements(By.CLASS_NAME, "serp-item__title-link-wrapper")

links_list = []
data = {}

for tag in list_of_vac_tag:
    links_tag = tag.find_element(By.CLASS_NAME, "bloko-link")
    links = links_tag.get_attribute("href")
    links_list.append(links)
# print(links_list)

for link in links_list:
    # print(link)
    browser.get(link)
    descriptions_tag = wait_element(browser, 1, By.CLASS_NAME, "vacancy-section")
    description = descriptions_tag.text.strip()
    # print(description)
    if 'Django' in description or 'Flask' in description:
        # print(link)
        info_tag = browser.find_element(By.CLASS_NAME, "vacancy-title")
        salary = info_tag.text.split('\n')[1].strip()
        # print(salary)
        company_tag = browser.find_element(By.CLASS_NAME, "vacancy-company-name")
        company = company_tag.text
        # print(company)
        city_tag = browser.find_element(By.CLASS_NAME, "magritte-text___tkzIl_4-1-4")
        city = city_tag.text.split(',')[0]
        # print(city)
        data[link] = {
            'salary': salary,
            'company': company,
            'city': city
        }
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

print(data)
browser.quit()