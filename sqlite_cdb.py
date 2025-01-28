from sqlite3 import connect

from read_config import read_card_info

def read_cdb(file, str_):
    conn = connect(file)
    try:
        cursor = conn.cursor()
        cursor.execute("select * from datas,texts where datas.id=texts.id")
        rows = cursor.fetchall()
        conn.close()


        if str_ == "rows":
            return rows
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
                    if row[i] == ot[0]:
                        card_data[-1][-1].append(ot[1])
            elif i == 3:
                setcard = []
                for a in range(4):
                    setcard.append(str(hex((row[i] >> (16 * a)) & 0xffff)).removeprefix('0x'))
                card_data[-1][-1].append(setcard)
            elif i == 4:
                type_list = []
                for type_ in card_info[7]:
                    if row[i] & type_[0] > 0:
                        type_list.append(True)
                    else:
                        type_list.append(False)
                card_data[-1][-1].append(type_list)
            elif i == 5 or i == 6:
                if (row[i] > -1):
                    card_data[-1][-1].append(row[i])
                else:
                    card_data[-1][-1].append('?')
            elif i == 7:
                level = ''
                for lv in card_info[3]:
                    if row[i] & 0xff == lv[0]:
                        level = lv[1]
                card_data[-1][-1].append([level, (row[i] >> 16) & 0xff])
            elif i == 8:
                for race in card_info[6]:
                    if row[i] == race[0]:
                        card_data[-1][-1].append(race[1])
            elif i == 9:
                for attribute in card_info[2]:
                    if row[i] == attribute[0]:
                        card_data[-1][-1].append(attribute[1])
            elif i == 10:
                category_list = []
                for category in card_info[5]:
                    if row[i] & category[0] > 0:
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

def change_cdb(row, file):
    opend = False
    try:
        conn = connect(file)
        opend = True
        cursor = conn.cursor()
        cursor.execute(f"INSERT OR REPLACE INTO datas VALUES({row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]});")
        cursor.execute(f"INSERT OR REPLACE INTO texts VALUES({row[11]}, '{row[12]}', '{row[13]}', '{row[14]}', '{row[15]}', '{row[16]}', '{row[17]}', '{row[18]}', '{row[19]}', '{row[20]}', '{row[21]}', '{row[22]}', '{row[23]}', '{row[24]}', '{row[25]}', '{row[26]}', '{row[27]}', '{row[28]}', '{row[29]}');")
        conn.commit()
        conn.close()
    except:
        if opend: conn.close()

def delete_cdb(card_id, file):
    opend = False
    try:
        conn = connect(file)
        opend = True
        cursor = conn.cursor()
        cursor.execute(f"Delete from datas where id='{card_id}';")
        cursor.execute(f"Delete from texts where id='{card_id}';")
        conn.commit()
        conn.close()
    except:
        if opend: conn.close()

def create_cdb(file):
    opend = False
    try:
        conn = connect(file)
        opend = True
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE texts(id integer primary key,name text,desc text,str1 text,str2 text,str3 text,str4 text,str5 text,str6 text,str7 text,str8 text,str9 text,str10 text,str11 text,str12 text,str13 text,str14 text,str15 text,str16 text);")
        cursor.execute("CREATE TABLE datas(id integer primary key,ot integer,alias integer,setcode integer,type integer,atk integer,def integer,level integer,race integer,attribute integer,category integer);")
        conn.commit()
        conn.close()
    except:
        if opend: conn.close()

if __name__ == '__main__':
    # row = read_cdb('d:\YGO\KoishiPro\cards.cdb', 'rows')[0]
    # print(row)
    # change_cdb(row, 'cdb_reader_example.cdb')
    delete_cdb(2511, 'cdb_reader_example.cdb')

