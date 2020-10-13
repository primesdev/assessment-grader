def get_id_number_string(number):
    value = str(number)
    id_string = {1: '000' + value,
     2: '00' + value,
     3: '0' + value,
     4: value}[len(value)]
    return id_string

def get_ids_from_names(names):
    ids = []
    id_no = 1
    id = ''
    for name in names:
        full_name = name.split()
        if len(full_name) == 1:
            id = full_name[0][:1]+get_id_number_string(id_no)
        else:
            id = full_name[0][:1] + full_name[1][:1] + get_id_number_string(id_no)
        ids.append(id)
        id_no += 1
    return ids
        
