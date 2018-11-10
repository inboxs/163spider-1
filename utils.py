def str_to_dict(datas):
    return dict({data[0].strip(): data[1].strip() for data in
     [data.split(":") for data in datas.split('\n') if data]})