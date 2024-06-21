
# 设置起始和结束ID
id_start = 10001
id_end = 114466

# 定义SQLite数据库文件路径
db_file = 'data_records.db'


def custom_pretty_print(obj, indent=0):
    def is_short_list(lst):
        return all(isinstance(item, (str, int, float)) and len(str(item)) < 20 for item in lst)
    
    def print_aligned_list(lst, indent):
        if all(isinstance(item, dict) for item in lst):
            keys = lst[0].keys()
            max_lens = {key: max(len(str(item[key])) for item in lst) for key in keys}
            header = ' '.join(f'{key:<{max_lens[key]}}' for key in keys)
            print(' ' * indent + header)
            for item in lst[:10]:
                row = ' '.join(f'{str(item[key]):<{max_lens[key]}}' for key in keys)
                print(' ' * indent + row)
            if len(lst) > 10:
                print(' ' * indent + '...')
        else:
            max_len = max(len(str(item)) for item in lst)
            row_len = 80 // (max_len + 2)
            for i in range(0, min(len(lst), 10), row_len):
                row_items = lst[i:i + row_len]
                print(' ' * indent + ' '.join(f'{str(item):<{max_len}}' for item in row_items))
            if len(lst) > 10:
                print(' ' * indent + '...')
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            print(' ' * indent + str(key) + ':')
            if isinstance(value, dict):
                custom_pretty_print(value, indent + 4)
            elif isinstance(value, list):
                if is_short_list(value):
                    print(' ' * indent + '[', ', '.join(map(str, value[:10])), ', ...]' if len(value) > 10 else ']')
                else:
                    if all(isinstance(item, dict) for item in value):
                        print_aligned_list(value, indent + 4)
                    else:
                        print(' ' * indent + '[')
                        for item in value[:10]:
                            if isinstance(item, dict):
                                custom_pretty_print(item, indent + 4)
                            else:
                                print(' ' * (indent + 4) + str(item) + ',')
                        if len(value) > 10:
                            print(' ' * (indent + 4) + '...')
                        print(' ' * indent + ']')
            else:
                print(' ' * (indent + 4) + str(value))
    elif isinstance(obj, list):
        if is_short_list(obj):
            print(' ' * indent + '[', ', '.join(map(str, obj[:10])), ', ...]' if len(obj) > 10 else ']')
        else:
            print(' ' * indent + '[')
            print_aligned_list(obj, indent + 4)
            print(' ' * indent + ']')
def custom_pretty_print(obj, indent=0, max_inline_length=20):
    def is_short_list(lst):
        return all(isinstance(item, (str, int, float)) and len(str(item)) < 20 for item in lst)

    def print_aligned_list(lst, indent):
        if all(isinstance(item, dict) for item in lst):
            keys = lst[0].keys()
            max_lens = {key: max(len(str(item[key])) for item in lst) for key in keys}
            header = ' '.join(f'{key:<{max_lens[key]}}' for key in keys)
            print(' ' * indent + header)
            for item in lst[:10]:
                row = ' '.join(f'{str(item[key]):<{max_lens[key]}}' for key in keys)
                print(' ' * indent + row)
            if len(lst) > 10:
                print(' ' * indent + '...')
        else:
            max_len = max(len(str(item)) for item in lst)
            row_len = 80 // (max_len + 2)
            for i in range(0, min(len(lst), 10), row_len):
                row_items = lst[i:i + row_len]
                print(' ' * indent + ' '.join(f'{str(item):<{max_len}}' for item in row_items))
            if len(lst) > 10:
                print(' ' * indent + '...')

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                print(' ' * indent + str(key) + ':')
                custom_pretty_print(value, indent + 4)
            elif isinstance(value, list):
                print(' ' * indent + str(key) + ':')
                if is_short_list(value):
                    print(' ' * indent + '[', ', '.join(map(str, value[:10])), ', ...]' if len(value) > 10 else ']')
                else:
                    if all(isinstance(item, dict) for item in value):
                        print_aligned_list(value, indent + 4)
                    else:
                        print(' ' * indent + '[')
                        for item in value[:10]:
                            if isinstance(item, dict):
                                custom_pretty_print(item, indent + 4)
                            else:
                                print(' ' * (indent + 4) + str(item) + ',')
                        if len(value) > 10:
                            print(' ' * (indent + 4) + '...')
                        print(' ' * indent + ']')
            else:
                # Print key-value pair in a single line if the combined length is short
                if len(str(key)) + len(str(value)) + 2 <= max_inline_length:
                    print(' ' * indent + f'{key}: {value}')
                else:
                    print(' ' * indent + str(key) + ':')
                    print(' ' * (indent + 4) + str(value))
    elif isinstance(obj, list):
        if is_short_list(obj):
            print(' ' * indent + '[', ', '.join(map(str, obj[:10])), ', ...]' if len(obj) > 10 else ']')
        else:
            print(' ' * indent + '[')
            print_aligned_list(obj, indent + 4)
            print(' ' * indent + ']')