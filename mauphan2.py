import tkinter as tk
from PIL import ImageTk, Image


def insert_image():
    # Thay đổi đường dẫn này để trỏ đến ảnh mới bạn muốn sử dụng
    new_image_path = "D:/5@ne/meme/chiu.jpg"
    new_image = Image.open(new_image_path)
    new_tk_image = ImageTk.PhotoImage(new_image)

    # Cập nhật hình ảnh label
    label.config(image=new_tk_image)
    label.image = new_tk_image


window = tk.Tk()
window.title("Chèn ảnh")
window.geometry('520x300')

# Tạo một label để hiển thị ảnh
label = tk.Label(window)
label.pack()

# Thêm nút "Chèn ảnh" để cập nhật ảnh
insert_button = tk.Button(window, text="Chèn ảnh", command=insert_image)
insert_button.pack()

# Thêm nút đóng cửa sổ
exit_button = tk.Button(window, text="Thoát", command=window.destroy)
exit_button.pack()

window.mainloop()

