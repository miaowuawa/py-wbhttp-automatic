def output_format(type,info):
    if type == 1:
        print("[Info]"+info)
    if type == 2:
        print("[Warning]"+info)
    if type == 3:
        print("[Error]"+info)
    if type == 4:
        print("[Notice]"+info)
