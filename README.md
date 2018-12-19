
# Парсер Авито

#### Для того чтобы запустить скрипт:

`git clone https://github.com/DimaKalbfleysh/Avito.git `

#### Потом запустить файл **main** и поменять параметры:

```python
city = cities["Ижевск"]  # Вместо "Ижевск", введите нужный Вам город

category = dict_categories["Велосипеды"] # Вместо "Велосипеды", ввидите нужную Вам категорию

direction = get_dict_district(city, list_ip)  # Если в city метро, то direction = get_metro(city, proxy_list)

district_or_metro = 'district'  # 'district' или 'metro'
 
number_of_threads = 5  # Количество потоков, чем больше, тем быстрее будет работать скрипт.
```