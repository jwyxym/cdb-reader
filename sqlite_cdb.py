from sqlite3 import connect

from read_config import read_card_info

def read_cdb(file, str_, _id = -1):
    conn = connect(file)
    try:
        cursor = conn.cursor()
        if int(_id) > -1:
            cursor.execute(f"SELECT datas.*, texts.* FROM datas, texts WHERE datas.id = texts.id and ( datas.id={_id}) ")
        else:
            cursor.execute("select * from datas,texts where datas.id=texts.id")
        rows = cursor.fetchall()
        conn.close()

        if str_ == "rows":
            return rows
        if str_ == "data":
            return get_data(rows[0], file)
        elif str_ == "list":
            return get_list(rows, file)

    except:
        conn.close()

    return []

def get_data(row, file):
    card_data = []
    card_info = read_card_info('./config/cardinfo_chinese.txt')
    for i in range(len(row)):
        if i == 1:
            for ot in card_info[1]:
                if row[i] == ot[0]:
                    card_data.append(ot[1])
        elif i == 3:
            setcard = []
            for a in range(4):
                setcard.append(str(hex((row[i] >> (16 * a)) & 0xffff)).removeprefix('0x'))
            card_data.append(setcard)
        elif i == 4:
            type_list = []
            for type_ in card_info[7]:
                if row[i] & type_[0] > 0:
                    type_list.append(True)
                else:
                    type_list.append(False)
            card_data.append(type_list)
        elif i == 5 or i == 6:
            if (row[i] > -1):
                card_data.append(row[i])
            else:
                card_data.append('?')
        elif i == 7:
            level = ''
            for lv in card_info[3]:
                if row[i] & 0xff == lv[0]:
                    level = lv[1]
            card_data.append([level, (row[i] >> 16) & 0xff])
        elif i == 8:
            for race in card_info[6]:
                if row[i] == race[0]:
                    card_data.append(race[1])
        elif i == 9:
            for attribute in card_info[2]:
                if row[i] == attribute[0]:
                    card_data.append(attribute[1])
        elif i == 10:
            category_list = []
            for category in card_info[5]:
                if row[i] & category[0] > 0:
                    category_list.append(True)
                else:
                    category_list.append(False)
            card_data.append(category_list)
        elif i == 14:
            card_hint = []
            for a in range(16):
                card_hint.append(row[i + a])
            card_data.append(card_hint)
            break
        else:
            card_data.append(row[i])
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

def add_cdb(file):
    card_id = int('1' + '0' * 10)
    opend = False
    try:
        conn = connect(file)
        opend = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT datas.*,texts.* FROM datas,texts WHERE datas.id=texts.id and ( datas.id={card_id} or datas.alias={card_id}) ")
        results = cursor.fetchall()
        while len(results) > 0:
            card_id += 1
            cursor.execute(f"SELECT datas.*,texts.* FROM datas,texts WHERE datas.id=texts.id and ( datas.id={card_id} or datas.alias={card_id}) ")
            results = cursor.fetchall()
        cursor.execute(f"INSERT INTO datas VALUES({card_id}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0});")
        cursor.execute(f"INSERT INTO texts VALUES({card_id}, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');")
        conn.commit()
        conn.close()
    except:
        if opend: conn.close()
        card_id = -1

    return card_id

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

def search_cdb(file, keyword):
    results = []
    opend = False
    try:
        conn = connect(file)
        opend = True
        cursor = conn.cursor()
        cursor.execute(get_select_SQL(keyword))
        results = cursor.fetchall()
        conn.close()
    except:
        if opend: conn.close()
    return get_list(results, file)

def get_select_SQL(k = []):
    key = "SELECT datas.*, texts.* FROM datas, texts WHERE datas.id = texts.id "
    if len(k) == 0:
        return key

    c_id = k[0]
    c_ot = k[1]
    c_alias = k[2]
    c_setcard = k[3]
    c_type = k[4]
    c_atk = k[5]
    c_def = k[6]
    c_level = k[7]
    c_race = k[8]
    c_attribute = k[9]
    c_category = k[10]
    c_name = k[11]
    c_desc = k[12]

    if c_name:
        if "%%" in c_name:
            c_name = c_name.replace("%%", "%")
        else:
            c_name = "%" + c_name.replace("%", "/%").replace("_", "/_") + "%"
        key += f" and texts.name like '{c_name.replace("'", "''")}' "

    if c_desc:
        key += f" and texts.desc like '%{c_desc.replace("'", "''")}%' "

    if c_ot > 0:
        key += f" and datas.ot = {c_ot} "

    if c_attribute > 0:
        key += f" and datas.attribute = {c_attribute} "

    if c_level & 0xff > 0:
        key += f" and (datas.level & 255) = {c_level & 0xff} "

    if c_level & 0xff000000 > 0:
        key += f" and (datas.level & 4278190080) = {c_level & 0xff000000} "

    if c_level & 0xff0000 > 0:
        key += f" and (datas.level & 16711680) = {c_level & 0xff0000} "

    if c_race > 0:
        key += f" and datas.race = {c_race} "

    if c_type > 0:
        key += f" and (datas.type & {c_type}) = {c_type} "

    if c_category > 0:
        key += f" and (datas.category & {c_category}) = {c_category} "

    if c_atk == -1:
        key += " and (datas.type & 1) = 1 and datas.atk = 0"
    elif c_atk != 0:
        key += f" and datas.atk = {c_atk} "

    if c_type & 0x4000000 > 0:
        key += f" and (datas.def & {c_def}) = {c_def} "
    else:
        if c_def == -1:
            key += " and (datas.type & 1) = 1 and datas.def = 0"
        elif c_def != 0:
            key += f" and datas.def = {c_def} "

    if c_id > 0 and c_alias > 0:
        key += f" and datas.id BETWEEN {c_alias} and {c_id} "
    elif c_id > 0:
        key += f" and (datas.id = {c_id} or datas.alias = {c_id}) "
    elif c_alias > 0:
        key += f" and datas.alias = {c_alias} "

    return key

# if __name__ == '__main__':
#     file = './example.cdb'
#     print(read_cdb(file, 'data', 2511))
