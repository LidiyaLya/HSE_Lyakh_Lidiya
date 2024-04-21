"""1. Найдите информацию об организациях.
a. Получите список ИНН из файла traders.txt.
b. Найдите информацию об организациях с этими ИНН в файле
traders.json.
c. Сохраните информацию об ИНН, ОГРН и адресе организаций из файла
traders.txt в файл traders.csv."""
import json
import csv
import re
with open("traders.txt", "r") as f:
    inns = [i.rstrip() for i in f.readlines()]
    with open("traders.json", "r") as f:
       Traders = json.load(f)
    traders = []
    for trader in Traders:
        if trader['inn'] in inns:
            traders.append(trader)
    with open('traders.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['INN', 'OGRN', 'ADDRESS'])
        for i in traders:
            writer.writerow([i['inn'], i['ogrn'], i['address']])

"""2. Напишите регулярное выражение для поиска email-адресов в тексте.
Для этого напишите функцию, которая принимает в качестве аргумента текст в виде
строки и возвращает список найденных email-адресов или пустой список, если
email-адреса не найдены.
Используйте датасет на 1 000 сообщений из ЕФРСБ для практики.
Текст сообщений можно найти по ключу msg_text.
Найдите все email-адреса в датасете и соберите их в словарь, где ключом будет
выступать ИНН опубликовавшего сообщение publisher_inn, а в значении будет
храниться множество set() с email-адресами."""

email_pattern = re.compile(r'\b[0-9a-zA-Z.-_]+@[0-9a-zA-Z.-_]+\.[a-zA-Z]+\b')
inn_org_pattern = re.compile(r'\b\d{10}\b')
inn_person_pattern = re.compile(r'\b\d{12}\b')

def find_emails():
    with open("10000_efrsb_messages.json", "r") as f:
        messages = json.load(f)
        results = {}
        for i in messages:
            emails = re.findall(email_pattern, i['msg_text'])
            for email in emails:
                email = email.lower()
                searched = results.get(i['publisher_inn'])
                if searched and email not in searched:
                    results[i['publisher_inn']].append(email)
                elif not searched:
                    new_item = {i['publisher_inn']: [email]}
                    results.update(new_item)
        inverted = {}
        for inn, emails in results.items():
            for email in emails:
                searched = inverted.get(email)
                if searched and inn not in searched:
                    inverted[email].append(inn)
                elif not searched:
                    new_item = {email: [inn]}
                    inverted.update(new_item)

        with open('emails.json', "w") as f:
            json.dump(results, f)
        print("stop")