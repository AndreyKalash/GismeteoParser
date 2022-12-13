from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def pictotxt(all_weath):
    for i in range(len(all_weath)): # переписка названий картинок (нормальный текст) в список all_weath
        picname = all_weath[i]
        if picname == '#d' or picname =='#n':
            all_weath[i] = 'Ясно'
        picname = picname.split('_')
        try:
            if picname[1] == 'c3':
                all_weath[i] = 'Пасмурно'
            elif picname[1] == 'c101':
                all_weath[i] = 'Переменная облачность' 
            elif picname[1] == 'c2':
                all_weath[i] = 'Облачно' 
            elif picname[1] == 'c1':
                all_weath[i] = 'Малооблачно' 
        except:
            all_weath[i] = all_weath[i]
        try:
            if picname[2] == 's2':
                all_weath[i] = all_weath[i] + ', снег'
            elif picname[2] == 's1':
                all_weath[i] = all_weath[i] + ', небольшой снег'
            elif picname[2] == 's3':
                all_weath[i] = all_weath[i] + ', сильный снег'
            elif picname[2] == 'r1':
                all_weath[i] = all_weath[i] + ', небольшой дождь'
            elif picname[2] == 'r2':
                all_weath[i] = all_weath[i] + ', дождь'
            elif picname[2] == 'r3':
                all_weath[i] = all_weath[i] + ', сильный дождь'
            elif picname[2] == 'rs1':
                all_weath[i] = all_weath[i] + ', небольшой мокрый снег'
            elif picname[2] == 'rs2':
                all_weath[i] = all_weath[i] + ', мокрый снег'
            elif picname[2] == 'rs3':
                all_weath[i] = all_weath[i] + ', сильный мокрый снег'

        except:
            all_weath[i] = all_weath[i]

    return all_weath


def get_detailed_info_otday(url): # подробный прогноз на ближайшие 10 дней
    options = Options()
    options.add_argument('headless') # закоментить для открывающихся окон браузера
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(chrome_options=options, service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(1) #ожидание 1 секунды

    
    day_info = [['00.00'], ['03.00'], ['06.00'],['09.00'],['12.00'],['15.00'],['18.00'],['21.00']]

    #поиск времени составленого прогноза
    div_time_info = driver.find_element(By.CLASS_NAME, value='widget-row.widget-row-time')  
    time_info = div_time_info.find_elements(By.CLASS_NAME, value='row-item')
    for ti in range(8):
        try:
            day_info[ti].append(time_info[ti].get_attribute('title'))
        except:
            day_info[ti].append('информация не доступна')

    #поиск погоды
    div_weath_info = driver.find_element(By.CLASS_NAME, value='widget-row.widget-row-icon')
    weath_info = div_weath_info.find_elements(By.TAG_NAME, value='use')
    weath_info_list = []
    for wi in range(8):
        weath_info_list.append(weath_info[wi].get_attribute('xlink:href'))
    # print(weath_info_list)
    weath_info_list = pictotxt(weath_info_list)
    for i in range(8):
        try:
            day_info[i].append(weath_info_list[i])
        except:
            None

    #поиск температуры
    div_temp_info = driver.find_element(By.CLASS_NAME, value='widget-row-chart-temperature')
    temp_info = div_temp_info.find_elements(By.CLASS_NAME, value='unit.unit_temperature_c')
    for tei in range(8):
        try:
            if temp_info[tei].text == '°C':
                day_info[tei].append(temp_info[tei+1].text)
            day_info[tei].append(temp_info[tei].text)
        except:
            day_info[tei].append('информация не доступна')

    #поиск средней скорости ветра м/с
    div_speed_info = driver.find_element(By.CLASS_NAME, value='widget-row-wind-speed')
    speed_info = div_speed_info.find_elements(By.CLASS_NAME, value='wind-unit.unit.unit_wind_m_s')
    for si in range(8):
        try:
            day_info[si].append(speed_info[si].text)
        except:
            day_info[si].append('информация не доступна')

    #поиск осадков в жидком эквиваленте, мм
    div_osadki_info = driver.find_element(By.CLASS_NAME, value='widget-row-precipitation-bars')
    osadki_info = div_osadki_info.find_elements(By.CLASS_NAME, value='item-unit')
    for oi in range(8):
        try:
            day_info[oi].append(osadki_info[oi].text)
        except:
            day_info[oi].append('информация не доступна')
    driver.quit()
    # print(day_info)
    return day_info


def weatherpars(сity): # погода на 50 дней
    options = Options()
    options.add_argument('--headless') # закоментить для открывающихся окон браузера
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(chrome_options=options , service=Service(ChromeDriverManager().install()))
    URL = 'https://www.gismeteo.ru/' #сыллка на главную страницу гисметео
    driver.get(URL)
    time.sleep(1)
    search = driver.find_element(By.CLASS_NAME, value='input.js-input') #поисковая строка
    search.click()
    search.send_keys(сity) #ввод в поисковую строку название города
    time.sleep(1)
    search.send_keys(Keys.ARROW_DOWN)
    search.send_keys(Keys.ENTER)
    get_url = driver.current_url
    get_month = get_url+'month' #переход на месячный прогноз по городу
    driver.get(get_month)

    all_temp = []
    all_days = []
    all_weath = []
    full_days = []

    div_temp = driver.find_element(By.CLASS_NAME, value='widget-body') #div с прогнозами на каждый день

    detailed_days = ['', 'tomorrow/', '3-day/', '4-day/', '5-day/', '6-day/', '7-day/', '8-day/','9-day/','10-day/']
    detailed_days_info = []
    for dd in range(len(detailed_days)):
        ddd = get_url+detailed_days[dd]
        day_info = get_detailed_info_otday(ddd) # подробный прогноз на ближайшие 10 дней
        detailed_days_info.append(day_info)

    temp = div_temp.find_elements(By.CLASS_NAME, value='unit.unit_temperature_c') 
    for t in temp[::2]:
        all_temp.append(t.text) #добавление температуры в список all_temp

    days = div_temp.find_elements(By.CLASS_NAME, value='date')
    for d in days:
        all_days.append(d.text) #добавление дат в список all_days

    for day in range(len(all_days)):
        d = all_days[day].split(' ')
        if len(d) == 2:
            all_days[day] = d[0] # переписка дат (только числа) в список all_days

    weath = div_temp.find_elements(By.TAG_NAME, value='use')
    for i in weath:
        all_weath.append(i.get_attribute('xlink:href')) #добавление названий картинок погоды в список all_weath

    all_weath = pictotxt(all_weath)
    
    for i in range(len(all_weath)):
        full_days.append([all_days[i], all_weath[i], all_temp[i]]) # добавление списков из даты, погоды, температуры в список full_days
    full_days_plus_detailed_days_info =[]

    full_days_plus_detailed_days_info.append(full_days)
    full_days_plus_detailed_days_info.append(detailed_days_info)

    driver.quit()
    return full_days_plus_detailed_days_info

# print(weatherpars('Москва')) # пример работы функции. для запуска раскоментить


