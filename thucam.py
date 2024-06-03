import pandas as pd

def read_data():
    return pd.read_csv('D:/Program Files/weblog.csv')


def display_lines(data, start, end):
    print(data.iloc[start:end])


def filter_invalid_logs(data):
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']
    return data[data['URL'].str.split().str[0].isin(valid_methods)]


def count_logs_by_date(data):

    data['Date'] = pd.to_datetime(data['Time'], format="%d/%b/%Y:%H:%M:%S").dt.date
    return data['Date'].value_counts()



def main():
    data = read_data()

    while True:
        print("\nMenu:")
        print("1. Hiển thị số dòng từ tệp dữ liệu")
        print("2. Lọc các dòng log bị lỗi")
        print("3. Đếm tổng số dòng log theo từng ngày")
        print("4. Thoát chương trình")

        choice = input("Chọn chức năng: ")

        if choice == '1':
            start = int(input("Nhập số dòng bắt đầu: "))
            end = int(input("Nhập số dòng kết thúc: "))
            display_lines(data, start, end)
        elif choice == '2':
            data = filter_invalid_logs(data)
            print("Đã lọc bỏ các dòng log bị lỗi.")
        elif choice == '3':
            log_counts = count_logs_by_date(data)
            print("Tổng số dòng log theo từng ngày:")
            print(log_counts)
        elif choice.lower() == 'exit' or choice == '4':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")


if __name__ == "__main__":
    main()
