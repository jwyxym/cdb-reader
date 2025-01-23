from sqlite3 import connect
from unittest import result

from read_config import read_card_info

def sql(file, str_):
    try:
        conn = connect(file)
        cursor = conn.cursor()
        cursor.execute("select * from datas,texts where datas.id=texts.id")
        rows = cursor.fetchall()
        conn.close()

        if str_ == "data":
            return get_data(rows, file)
        elif str_ == "list":
            return get_list(rows, file)

    except:
        conn.close()

    return []

def get_data(rows, file):
    card_data = [[file[file.rfind('/') + 1 : ]], []]
    card_info = read_card_info('./config/cardinfo_chinese.txt')
    for row in rows:
        if len(card_data[-1]) ==  10:
            card_data.append([])
        card_data[-1].append([])
        for i in range(len(row)):
            if i == 1:
                for ot in card_info[1]:
                    if row[i] == int(ot[0], 16):
                        card_data[-1][-1].append(ot[1])
            elif i == 3:
                number = str(hex(row[i])).removeprefix('0x')
                if len(number) > 16:
                    number = number[-16 : ]
                if len(number) < 16:
                    number = '0' * (16 - (len(number))) + number
                result = []
                for a in range(len(number), 0, -4):
                    setcard = number[a - 4 : a].lstrip('0')
                    if len(setcard) == 0:
                        setcard = '0'
                    result.append(setcard)
                card_data[-1][-1].append((result))
            elif i == 4:
                type_list = []
                for type_ in card_info[6]:
                    if row[i] & int(type_[0], 16) > 0:
                        type_list.append(True)
                    else:
                        type_list.append(False)
                card_data[-1][-1].append(type_list)
            elif i == 7:
                level = ''
                for lv in card_info[3]:
                    if row[i] & 0xff == int(lv[0], 16):
                        level = lv[1]
                card_data[-1][-1].append([level, (row[i] >> 16) & 0xff])
            elif i == 8:
                for race in card_info[5]:
                    if row[i] == int(race[0], 16):
                        card_data[-1][-1].append(race[1])
            elif i == 9:
                for attribute in card_info[2]:
                    if row[i] == int(attribute[0], 16):
                        card_data[-1][-1].append(attribute[1])
            elif i == 10:
                category_list = []
                for category in card_info[4]:
                    if row[i] & int(category[0], 16) > 0:
                        category_list.append(True)
                    else:
                        category_list.append(False)
                card_data[-1][-1].append(category_list)
            elif i == 14:
                card_hint = []
                for a in range(16):
                    card_hint.append(row[i + a])
                card_data[-1][-1].append(card_hint)
                break
            else:
                card_data[-1][-1].append(row[i])
    return card_data

def get_list(rows, file):
    card_list = [[file[file.rfind('/') + 1 : ]], []]
    for row in rows:
        if len(card_list[-1]) ==  10:
            card_list.append([])
        card_list[-1].append(f'{str(row[0])} {row[12]}')
    return card_list

if __name__ == '__main__':
    file = 'd:/YGO/KoishiPro/cards.cdb'
    str_ = 'data'
    result = sql(file, str_)
