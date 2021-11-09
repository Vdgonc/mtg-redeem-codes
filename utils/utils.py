def load_code_list_file(file_name) -> list:
    code_list = []
    with open(file_name, 'r') as f:
        codes = f.read().split('\n')

        for d in codes:
            code_list.append(d)

    return code_list
