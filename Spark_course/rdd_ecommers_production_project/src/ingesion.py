def read_file(sc,file_path):
    raw_rdd = sc.textFile(file_path)
    return raw_rdd

def remove_header(raw_rdd):
    header = raw_rdd.first()
    act_data = raw_rdd.filter(lambda row:row != header)
    return header,act_data    