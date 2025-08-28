import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys('kireevd14@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('51151013Dd')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    driver.find_element(By.CLASS_NAME, 'nav-link').click()
    assert driver.find_element(By.ID, 'all_my_pets')
    yield driver

    driver.quit()




#----------------------------------------------------------------------------------------------------------------------#
#1.Присутствуют все питомцы.
def test_check_pets_users(driver):
    pets_number = int(driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1])
    rows_pets= WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#all_my_pets table.table.table-hover tbody tr"))
    )
    assert pets_number == len(rows_pets)




#----------------------------------------------------------------------------------------------------------------------#
#2.Хотя бы у половины питомцев есть фото.
def test_photos_of_users_pets(driver):
    images = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#all_my_pets table tbody tr img"))
    )
    no_photo = 0
    photo = 0
    images_list = []
    #images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets table tbody tr th img')

    for i in range(len(images)):
        images_list.append(images[i])
        if images[i].get_attribute('src') != '':
            photo += 1
        else:
            no_photo += 1

    # Проверка: хотя бы у половины питомцев есть фото
    assert photo > len(images) / 2
    #|if photo > no_photo:
    #|    print(f"\nБольше чем у половины питомцев присутствует фото\nУ {photo} из {len(images_list)} питомцев присутствует фото\nКоличество питомцев у которых есть фото : {photo}\nКоличество питомцев без фото : {no_photo}")
    #|elif photo<no_photo:
    #|    print(f"\nБольше чем у половины питомцев отсутствует фото\nУ {photo} из {len(images_list)} питомцев присутствует фото\nКоличество питомцев у которых есть фото : {photo}\nКоличество питомцев без фото : {no_photo}")
    #|else:
    #|    print(f"\nУ половины пиомцев из списка отсутствует фото \nУ {photo} из {len(images_list)} питомцев присутствует фото")




#----------------------------------------------------------------------------------------------------------------------#
#3.У всех питомцев есть имя, возраст и порода.
def test_name_age_breed(driver):
    rows_pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#all_my_pets table.table tbody tr"))
    )
    #rows_pets = driver.find_elements(By.CSS_SELECTOR, "div#all_my_pets table.table tbody tr")
    names, breeds, ages = [], [], []

    for row in rows_pets:
        driver.implicitly_wait(10)
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 0 and cells[0].text.strip():
            names.append(cells[0].text.strip())
        if len(cells) > 1 and cells[1].text.strip():
            breeds.append(cells[1].text.strip())
        if len(cells) > 2 and cells[2].text.strip():
            ages.append(cells[2].text.strip())
    print(f'количество имен: {len(names)}, пород: {len(breeds)}, и возростов: {len(ages)} во всех карточках питомцев')
    assert len(names) == len(rows_pets) and len(breeds) == len(rows_pets) and len(ages) == len(rows_pets)
    #if len(names) == len(rows_pets) and len(breeds) == len(rows_pets) and len(ages) == len(rows_pets):
    #    print('у каждого питомца есть имя, порода и возраст')
    #else:
    #    print('не у всех питомцев указыны: порода, возраст и имя ')




#----------------------------------------------------------------------------------------------------------------------#
#4.У всех питомцев разные имена.
def test_names_pets(driver):
    names_pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
    )
    #names_pets= driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    names = [name.text for name in names_pets]
    print(names)
    assert len(names) == len(set(names)), "Есть повторяющиеся имена питомцев!"




#----------------------------------------------------------------------------------------------------------------------#
#5.В списке нет повторяющихся питомцев. (Сложное задание).
def test_duplicates_pets(driver):
    pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr'))
    )
    #pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    pets_data = [pet.text for pet in pets if pet.text != ""]

    assert len(pets_data) == len(set(pets_data)), "Есть повторяющиеся карточки питомцев!"





# Я не понял "driver.implicitly_wait(10)" нужно вставлять при обозначении драйвера и сайта (def driver), или в уже в тестах каждый раз перед поиском определенного объекта ?

#   И как добавлять явные ожидания тоже например в первом тесте(test_check_pets_users):
#   def test_check_pets_users(driver):
#     pets_number = int(driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1])
#
#     rows_pets = WebDriverWait(driver, 10).until(
# EC.presence_of_element_located((By.CSS_SELECTOR, "div#all_my_pets table.table.table-hover tbody tr"))
# )
#     assert pets_number == len(rows_pets)
# все сразу ломается же




# python3 -m pytest -v --driver Chrome tests/test_pets_user.py