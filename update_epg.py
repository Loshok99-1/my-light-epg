import xml.etree.ElementTree as ET
import urllib.request
import gzip
import os

# 1. СПИСОК ВАШИХ КАНАЛОВ (пишите названия точно как в вашем списке)
TARGET_CHANNELS = [
    "Первый канал", "Россия 1", "Матч ТВ", "НТВ", "Пятый канал", 
    "Россия К", "Россия 24", "Карусель", "ОТР", "ТВ Центр", 
    "РЕН ТВ", "Спас", "СТС", "Домашний", "ТВ-3", "Пятница", 
    "Звезда", "Мир", "ТНТ", "Муз-ТВ", "Москва 24", "Ю", "2х2"
]

SOURCE_URL = "http://www.teleguide.info/download/new3/xmltv.xml.gz"

def main():
    print("Загрузка и распаковка...")
    urllib.request.urlretrieve(SOURCE_URL, "source.xml.gz")
    with gzip.open("source.xml.gz", 'rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()

    # Словарь для соответствия Название -> ID
    name_to_id = {}
    for chan in root.findall('channel'):
        c_id = chan.get('id')
        for name_tag in chan.findall('display-name'):
            name = name_tag.text.strip()
            if name in TARGET_CHANNELS:
                name_to_id[name] = c_id

    print(f"Найдено соответствий: {len(name_to_id)} из {len(TARGET_CHANNELS)}")

    # Создаем новый XML
    new_root = ET.Element('tv')
    new_root.attrib = root.attrib

    # Добавляем только найденные каналы
    found_ids = set(name_to_id.values())
    for chan in root.findall('channel'):
        if chan.get('id') in found_ids:
            new_root.append(chan)

    # Добавляем программы для этих каналов
    for prog in root.findall('programme'):
        if prog.get('channel') in found_ids:
            new_root.append(prog)

    new_tree = ET.ElementTree(new_root)
    new_tree.write("epg.xml", encoding='utf-8', xml_declaration=True)
    print("Файл epg.xml успешно обновлен!")

if __name__ == "__main__":
    main()
