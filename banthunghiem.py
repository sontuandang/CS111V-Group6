import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def show_picture():
    global image_path
    image_path = filedialog.askopenfilename()
    if image_path:
        display_image()


def display_image():
    global image, tk_image, buttons, current_angle
    image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(image)
    current_angle = 0

    canvas.delete("all")  # Xóa tất cả các vật thể trước khi vẽ hình ảnh mới

    # Tính toán tọa độ để hiển thị ảnh ở trung tâm canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    img_width = tk_image.width()
    img_height = tk_image.height()
    x = (canvas_width - img_width) // 2
    y = (canvas_height - img_height) // 2

    canvas.create_image(x, y, anchor="nw", image=tk_image)
    canvas.image = tk_image  # Giữ tham chiếu để hình ảnh không bị hủy bỏ

    # Thêm các nút vào hình ảnh
    buttons = []
    buttons.append(tk.Button(canvas, text="Xoay ảnh", command=rotate_image))
    buttons.append(tk.Button(canvas, text="Xoay trái", command=rotated_image))
    buttons.append(tk.Button(canvas, text="Chức năng 3"))
    buttons.append(tk.Button(canvas, text="Chức năng 4"))

    y_offset = 10
    for button in buttons:
        canvas.create_window(3, y_offset, anchor="nw", window=button)
        y_offset += 30


def rotate_image():
    global image, tk_image, buttons, current_angle
    if image:
        current_angle += 90
        current_angle %= 360  # Đảm bảo góc xoay nằm trong khoảng từ 0 đến 359 độ
        rotated_image = image.rotate(current_angle)  # Xoay hình ảnh theo góc mới
        tk_image = ImageTk.PhotoImage(rotated_image)
        canvas.delete("all")  # Xóa hình ảnh hiện tại

        # Tính toán tọa độ để hiển thị ảnh ở trung tâm canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        img_width = tk_image.width()
        img_height = tk_image.height()
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2

        canvas.create_image(x, y, anchor="nw", image=tk_image)
        canvas.image = tk_image  # Giữ tham chiếu

        # Hiển thị lại các nút chức năng
        y_offset = 10
        for button in buttons:
            canvas.create_window(3, y_offset, anchor="nw", window=button)
            y_offset += 30


def rotated_image():
    global image, tk_image, buttons, current_angle
    if image:
        current_angle -= 90
        current_angle %= 360  # Đảm bảo góc xoay nằm trong khoảng từ 0 đến 359 độ
        rotate_image = image.rotate(current_angle)  # Xoay hình ảnh theo góc mới
        tk_image = ImageTk.PhotoImage(rotate_image)
        canvas.delete("all")  # Xóa hình ảnh hiện tại

        # Tính toán tọa độ để hiển thị ảnh ở trung tâm canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        img_width = tk_image.width()
        img_height = tk_image.height()
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2

        canvas.create_image(x, y, anchor="nw", image=tk_image)
        canvas.image = tk_image  # Giữ tham chiếu

        # Hiển thị lại các nút chức năng
        y_offset = 10
        for button in buttons:
            canvas.create_window(3, y_offset, anchor="nw", window=button)
            y_offset += 30


root = tk.Tk()
root.title("Image with Buttons")
root.state('zoomed')

canvas = tk.Canvas(root, width=4000, height=600)
canvas.pack(expand=True, fill=tk.BOTH)

open_image_button = tk.Button(root, text="Open Image", command=show_picture)
open_image_button.pack()

exit_image_button = tk.Button(root, text="Exit", command=root.destroy)
exit_image_button.pack()

image_path = None
image = None
tk_image = None
buttons = []
current_angle = 0

root.mainloop()