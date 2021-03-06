import math
import data_loader
array_spliter_d1 = '|'
array_spliter_d2 = ';'
dict_spliter_d1 = '#'
dict_spliter_d2 = '='
def array_process(data, var_type):
    new_data = []
    data_loader.Cell.array_index = [0, 0]
    if array_spliter_d2 in data:
        for i in data.split(array_spliter_d1):
            if i != '':
                data_loader.Cell.array_index[0] += 1
                temp = []
                for j in i.split(array_spliter_d2):
                    data_loader.Cell.array_index[1] += 1
                    temp.append(var_type(j))
                data_loader.Cell.array_index[1]=0
                new_data.append(temp)
    else:
        for i in data.split(dict_spliter_d1):
            if i != '':
                data_loader.Cell.array_index[0] += 1
                new_data.append(var_type(i))
    data_loader.Cell.array_index=''
    return new_data


def var_int(data):
    return int(data)


def var_float(data):
    return int(float(data)*1000000)


def var_number(data):
    return int(data) if math.modf(float(data))[0] == 0 else float(data)


def var_string(data):
    return str(data)


def var_text(data):
    key = data_loader.text_key_str()
    data_loader.Work.localization.execute(
        "INSERT OR REPLACE into Localization (key,version,origin) values ('%s','%s','%s')" % (key, data_loader.Work.version, str(data)))
    data_loader.Work.localization.commit()
    return key


def array_int(data):
    return array_process(data, var_int)


def array_float(data):
    return array_process(data, var_float)


def array_number(data):
    return array_process(data, var_number)


def array_string(data):
    return array_process(data, str)


def array_text(data):
    return array_process(data, var_text)


def key_int(data):
    return int(data)


def key_string(data):
    return str(data)


def dictionary(data):
    import re
    output = {}
    for element in data.split(dict_spliter_d1):
        part=re.search(r'\[([a-zA-Z]+)([0-9]*)\](.+)'+ dict_spliter_d2 + '(.+)',element)
        field_type = part.group(1)
        field_name = int(part.group(3)) if part.group(
            3).isdigit() else part.group(3)
        filed_value = part.group(4)
        if field_type=='t' or field_type=='at':
            data_loader.Cell.dict_key=field_name
        else:
            data_loader.Cell.dict_key= ''
        output[field_name] = process_type[field_type](filed_value)
    data_loader.Cell.dict_key= ''
    return output

process_type = {
    "i": var_int,
    "f": var_float,
    "n": var_number,
    "s": var_string,
    "t": var_text,
    "ai": array_int,
    "af": array_float,
    "an": array_number,
    "as": array_string,
    "at": array_text,
    "d": dictionary,
    "ikey": key_int,
    "skey": key_string,
}