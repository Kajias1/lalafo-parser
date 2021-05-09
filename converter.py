import json
import csv

# Converting a json string into the csv document
def convert(data: str):
    file_name = 'lalafo_parse.csv'

    with open(file_name, 'w') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(['Заголовок', 'Стоимость', 'Активность', 'Номер'])
        for item in data:
            csv_file.writerow([
                item['Заголовок'],
                item['Стоимость'],
                item['Активность'],
                item['Номер'],
            ])
