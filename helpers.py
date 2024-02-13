from datetime import datetime

def convert_date(date_str):
    date_li = date_str.split('-')
    date_li = [int(item) for item in date_li]
    return datetime(date_li[0], date_li[1], date_li[2])

if __name__ == "__main__":
    print(convert_date('2023-02-13'))