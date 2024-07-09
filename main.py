import json
import requests
import bs4
from fake_headers import Headers


def get_data(soup, link):
    title = soup.find('h1', {'data-qa': "vacancy-title"}).text
    temp_salary = soup.find('div', {'data-qa': "vacancy-salary"})
    if temp_salary:
        salary = temp_salary.text
    else:
        salary = 'Уровень дохода не указан'
    company = soup.find('a', {'data-qa': "vacancy-company-name"}).text
    temp_city = soup.find('span', {'data-qa': "vacancy-view-raw-address"})
    if temp_city:
        city = temp_city.text
    else:
        city = soup.find('p', {'data-qa': "vacancy-view-location"}).text
    vac_dict = {
        "Title": title,
        "Link": link,
        "Salary": salary,
        "Company name": company,
        "City": city
    }
    return vac_dict


def get_headers():
    return Headers(browser='chrome', os='win').generate()


main_response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=get_headers())
main_html = main_response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')
vacancies = main_soup.find('div', id="a11y-main-content")
vacancies_list = vacancies.find_all('a', class_="bloko-link", target="_blank")
vacancies_filtered = []
for vacancy in vacancies_list:
    vac_link = vacancy.get('href')
    vac_response = requests.get(f"{vac_link}", headers=get_headers())
    vac_html = vac_response.text
    vac_soup = bs4.BeautifulSoup(vac_html, 'lxml')
    vac_content = vac_soup.find('div', {'data-qa': "vacancy-description"})
    if vac_content:
        vac_text = vac_content.text
        if "Django" in vac_text and "Flask" in vac_text:
            vacancies_filtered.append(get_data(vac_soup, vac_link))

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies_filtered, f, ensure_ascii=False, indent=4)
