import xml.etree.ElementTree as ET
import urllib.request
import gzip
import os

# Конфигурация
SOURCE_URL = "http://www.teleguide.info/download/new3/xmltv.xml.gz"
NEEDED_CHANNELS = ["1", "2", "4", "255", "676", "1000", "10", "103", "12", "104", "102", "105", "1671", "330", "203", "1093", "288", "156", "106", "503", "557", "1487", "1422", "1737", "39", "8", "276"]

def main():
    print("Загрузка...")
    urllib.request.urlretrieve(SOURCE_URL, "source.xml.gz")
    
    print("Распаковка...")
    with gzip.open("source.xml.gz", 'rb') as f_in:
        tree = ET.parse(f_in)
        root = tree.getroot()

    new_root = ET.Element('tv')
    new_root.attrib = root.attrib

    # Фильтруем
    for channel in root.findall('channel'):
        if channel.get('id') in NEEDED_CHANNELS:
            new_root.append(channel)

    for programme in root.findall('programme'):
        if programme.get('channel') in NEEDED_CHANNELS:
            new_root.append(programme)

    print("Сохранение...")
    new_tree = ET.ElementTree(new_root)
    new_tree.write("epg.xml", encoding='utf-8', xml_declaration=True)
    print("Готово!")

if __name__ == "__main__":
    main()
