# ЗАДАЧА - Поиск вакансии "Энергетик" с зараплатой минимум 
# 100 000 рублей в регионе "Челябинская область" (код 74)

# 1. Импорт библиотек и ссылок
import requests
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import csv

# 2. Проверка запроса от сайта труд всем
answer.status_code

# 3. Просмотр полученного текста
answer.text
# 4. Получаем JSON
dct_vacs = answer.json()
print(dct_vacs)


# 5. Просмотр ключей словаря
dct_vacs.keys()

# 6. Анализ ключей
for key, value in dct_vacs.items():
    print(f'Ключ----<<{key}>>----')
    print(value)
    print('--' * 10)

# 7. Анализ типа данных и преобразование к понятному содержимому
dct_vacs.get('results')

# 8. Получается, что название вакансии 
# 'job-name', и зарплата 'salary_min' находятся внутри {'vacancies'} и защиты в список
vacancy_data = dct_vacs['results'].get('vacancies')
type(vacancy_data)
vacancy_data[0]

# 9. Собираем словарь с нужными пунктами для отбора и базовый список
dct_one = {
	'job-name': None,
    'salary': None,
	'salary_min': None,
    'salary_max': None,
    'company': None,
    'addresses': None,
    'vac_url': None}
 
lst_dict = []
vacancy_dict = dct_one.copy()  # создаем один раз копию для переиспользования

# 10. Выполняем обход с помощью цикла for по всем вакансиям

dct_one = {
    'job-name': None,
    'salary': None,
    'salary_min': None,
    'salary_max': None,
    'company_name': None,      # ← сразу строка, а не словарь
    'address_location': None,  # ← сразу строка, а не словарь
    'vac_url': None
}

lst_dict = []

for vacancy_item in vacancy_data:
    vacancy_dict = dct_one.copy()
    vac = vacancy_item['vacancy']
    
    # Простые поля
    vacancy_dict['job-name'] = vac.get('job-name')
    vacancy_dict['salary'] = vac.get('salary', 0)
    vacancy_dict['salary_min'] = vac.get('salary_min', 0)
    vacancy_dict['salary_max'] = vac.get('salary_max', 0)
    vacancy_dict['vac_url'] = vac.get('vac_url', None)
    
    # Извлекаем название компании
    company = vac.get('company')
    vacancy_dict['company_name'] = company.get('name') if company else None
    
    # Извлекаем адрес
    addresses = vac.get('addresses')
    if addresses and addresses.get('address'):
        vacancy_dict['address_location'] = addresses['address'][0].get('location')
    else:
        vacancy_dict['address_location'] = None
    
    lst_dict.append(vacancy_dict)
    
    # Добавляем заполненный словарь в список
    lst_dict.append(vacancy_dict.copy())

# 11. Проверяем как собрался список
print(lst_dict[17])

# 12. Назначем DataFrame для наглядности
df = pd.DataFrame(lst_dict)
print(df.head())

# 13. С применением пагинации (по всем вакансиям в регионе)¶

offset_number = 0
region_code = 74

dct_one = {
	'job-name': None,
    'salary': None,
	'salary_min': None,
    'salary_max': None,
    'company': None,
    'addresses': None,
    'vac_url': None}
 
lst_dict = []

for offset_number in tqdm(range (0,123)):
    link_pag = f'http://opendata.trudvsem.ru/api/v1/vacancies/region/74?offset={offset_number}'
    answer = requests.get(link_pag)
    time.sleep(5)
    print(link_pag)
    if answer.status_code == 200:
        dct_vacs = answer.json()
        dct_vacs.get('results')
        vacancy_data = dct_vacs['results'].get('vacancies')
        for vacancy_item in vacancy_data:
            vacancy_dict = dct_one.copy()
            vac = vacancy_item['vacancy']
            
            # Простые поля
            vacancy_dict['job-name'] = vac.get('job-name')
            vacancy_dict['salary'] = vac.get('salary', 0)
            vacancy_dict['salary_min'] = vac.get('salary_min', 0)
            vacancy_dict['salary_max'] = vac.get('salary_max', 0)
            vacancy_dict['vac_url'] = vac.get('vac_url', None)
            
            # Извлекаем название компании
            company = vac.get('company')
            vacancy_dict['company_name'] = company.get('name') if company else None
            
            # Извлекаем адрес
            addresses = vac.get('addresses')
            if addresses and addresses.get('address'):
                vacancy_dict['address_location'] = addresses['address'][0].get('location')
            else:
                vacancy_dict['address_location'] = None
            
            lst_dict.append(vacancy_dict)

offset_number = 0
region_code = 74

# ===== В dct_one ДОЛЖНЫ БЫТЬ ВСЕ ПОЛЯ, КОТОРЫЕ МЫ ИСПОЛЬЗУЕМ =====
dct_one = {
    'job-name': None,
    'salary': None,
    'salary_min': None,
    'salary_max': None,
    'company_name': None,
    'address_location': None,
    'vac_url': None
}
 
lst_dict = []

# ===== ИМПОРТ CSV =====
import csv

# ===== ОТКРЫВАЕМ ФАЙЛ ДЛЯ ЗАПИСИ =====
try:
    with open('vacancies.csv', 'w', newline='', encoding='utf-8') as file:
        columns = ['job-name', 'salary', 'salary_min', 'salary_max', 
                   'company_name', 'address_location', 'vac_url']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        file.flush()  # Сразу записываем заголовки на диск
        print('Файл vacancies.csv создан, заголовки записаны')
        
        for offset_number in tqdm(range(0, 123)):
            try:
                link_pag = f'http://opendata.trudvsem.ru/api/v1/vacancies/region/74?offset={offset_number}'
                answer = requests.get(link_pag, timeout=30)
                time.sleep(5)
                print(link_pag)
                
                if answer.status_code == 200:
                    dct_vacs = answer.json()
                    vacancy_data = dct_vacs.get('results', {}).get('vacancies', [])
                    
                    for vacancy_item in vacancy_data:
                        try:
                            vacancy_dict = dct_one.copy()
                            vac = vacancy_item.get('vacancy', {})
                            
                            # Простые поля
                            vacancy_dict['job-name'] = vac.get('job-name')
                            vacancy_dict['salary'] = vac.get('salary', 0)
                            vacancy_dict['salary_min'] = vac.get('salary_min', 0)
                            vacancy_dict['salary_max'] = vac.get('salary_max', 0)
                            vacancy_dict['vac_url'] = vac.get('vac_url', None)
                            
                            # Извлекаем название компании
                            company = vac.get('company')
                            vacancy_dict['company_name'] = company.get('name') if company else None
                            
                            # Извлекаем адрес
                            addresses = vac.get('addresses')
                            if addresses and addresses.get('address'):
                                vacancy_dict['address_location'] = addresses['address'][0].get('location')
                            else:
                                vacancy_dict['address_location'] = None
                            
                            # ===== ФИЛЬТРАЦИЯ ПО СЛОВУ "энергетик" =====
                            job_name = vacancy_dict['job-name'] or ''
                            if 'энергетик' in job_name.lower():
                                lst_dict.append(vacancy_dict)
                                
                                if len(lst_dict) >= 100:
                                    writer.writerows(lst_dict)
                                    file.flush()  # ПРИНУДИТЕЛЬНО ЗАПИСЫВАЕМ НА ДИСК
                                    print(f'✅ Сохранено 100 вакансий с "энергетик" (всего в файле: пока не считано)')
                                    lst_dict.clear()
                        
                        except Exception as e:
                            print(f'⚠️ Ошибка при обработке вакансии: {e}')
                            continue
                
                else:
                    print(f'❌ Ошибка запроса: статус {answer.status_code} для {link_pag}')
            
            except requests.exceptions.RequestException as e:
                print(f'🌐 Ошибка сети при запросе {link_pag}: {e}')
                continue
            
            except Exception as e:
                print(f'💥 Неожиданная ошибка при обработке страницы {offset_number}: {e}')
                # Сохраняем то, что уже напарсили
                if lst_dict:
                    writer.writerows(lst_dict)
                    file.flush()  # ПРИНУДИТЕЛЬНО ЗАПИСЫВАЕМ НА ДИСК
                    print(f'💾 Сохранено {len(lst_dict)} вакансий перед ошибкой')
                    lst_dict.clear()
                continue
        
        # ===== СОХРАНЯЕМ ОСТАВШИЕСЯ ВАКАНСИИ =====
        if lst_dict:
            writer.writerows(lst_dict)
            file.flush()  # ПРИНУДИТЕЛЬНО ЗАПИСЫВАЕМ НА ДИСК
            print(f'💾 Сохранено последние {len(lst_dict)} вакансий с "энергетик"')
            lst_dict.clear()
        
        print(f'📁 Файл сохранен: vacancies.csv')
        print(f'📊 Размер файла: {os.path.getsize("vacancies.csv") / 1024:.2f} КБ')

except Exception as e:
    print(f'🔥 КРИТИЧЕСКАЯ ОШИБКА: {e}')
    # Пытаемся сохранить то, что успели напарсить
    try:
        if lst_dict:
            with open('vacancies_backup.csv', 'w', newline='', encoding='utf-8') as backup_file:
                backup_writer = csv.DictWriter(backup_file, fieldnames=columns)
                backup_writer.writeheader()
                backup_writer.writerows(lst_dict)
            print(f'💾 Сохранено {len(lst_dict)} вакансий в backup файл vacancies_backup.csv')
    except:
        print('❌ Не удалось сохранить backup')

print('🏁 Сбор данных завершен!')

# 14. Проверка сохранения данных в списке

print(lst_dict[123])

# 15. Сохранение данных из списка в csv 

name_file = 'вакансии_74_регион.csv'

if lst_dict:
    fieldnames = list(lst_dict[0].keys())
    
    # Используем utf-8-sig для совместимости с Excel
    if os.path.isfile(name_file):
        with open(name_file, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(lst_dict)
    else:
        with open(name_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(lst_dict)
    
    print(f"Данные сохранены в файл: {name_file}")
    print(f"Всего записей: {len(lst_dict)}")
else:
    print("Нет данных для сохранения")

# 17. Собираем DataFrame для наглядности 
# (в csv лишние колонки влезли, исключил их)¶

df = pd.read_csv('C:/Users/D/вакансии_74_регион_total.csv',
                 sep=';',
                 encoding='utf-8',
                 quotechar='"',
                 doublequote=True)  # обрабатывать двойные кавычки
df.head()

# 18. Ввожу фильтр по названию вакансии энергетик и зарплате 100000¶

flt = (df['salary_min'] >= 100000) & (df['job-name'].str.contains(r'\bэнергетик\b', case=False, na=False))
df[flt]

# ИТОГ - всего одна вакансия, ужас, как низко нас ценят.
