import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageEnhance

def show_picture():
    global image_path, original_image, current_image
    image_path = filedialog.askopenfilename()
    if image_path:
        original_image = Image.open(image_path)
        current_image = original_image.copy()
        display_image(original_image)

def display_image(image):
    global tk_image
    tk_image = ImageTk.PhotoImage(image)

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
    num_buttons = len(buttons)
    button_height = 30
    spacing = 10
    total_height = num_buttons * button_height + (num_buttons - 5) * spacing
    start_y = (canvas_height - total_height) // 2

    for i, button in enumerate(buttons):
        button_y = start_y + i * (button_height + spacing)
        canvas.create_window(10, button_y, anchor="nw", window=button, width=100, height=button_height)

def rotate_image():
    global current_image
    if current_image:
        rotated_image = current_image.rotate(90, expand=True)
        display_image(rotated_image)
        current_image = rotated_image

def rotate_image_left():
    global current_image
    if current_image:
        rotated_image = current_image.rotate(-90, expand=True)
        display_image(rotated_image)
        current_image = rotated_image

def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        apply_color(color)

def apply_color(color):
    global current_image
    if current_image:
        # Tạo ảnh đen trắng từ ảnh gốc để giữ lại chi tiết
        grayscale_image = current_image.convert("L")

        # Tạo một ảnh mới với màu đã chọn và cùng kích thước
        color_image = Image.new("RGB", current_image.size, color)

        # Kết hợp ảnh màu và ảnh đen trắng để giữ lại chi tiết
        colored_image = ImageEnhance.Color(grayscale_image).enhance(0.0)
        colored_image = Image.blend(colored_image.convert("RGB"), color_image, alpha=0.5)

        display_image(colored_image)
        current_image = colored_image

def reset_image():
    global original_image, current_image
    if original_image:
        current_image = original_image.copy()
        display_image(original_image)


def save_image():
    global current_image
    if current_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            current_image.save(save_path)


root = tk.Tk()
root.title("Image with Buttons")
root.state('zoomed')


# Thêm biểu tượng vào cửa sổ
icon_path = 'Shiroko.png'  # Đặt đường dẫn tới tệp .ico ở đây
icon_image = ImageTk.PhotoImage(file=icon_path)
root.iconphoto(False, icon_image)


canvas = tk.Canvas(root, width=4000, height=600)
canvas.pack(expand=True, fill=tk.BOTH)

open_image_button = tk.Button(root, text="Open Image", command=show_picture)
open_image_button.pack()

exit_image_button = tk.Button(root, text="Exit", command=root.destroy)
exit_image_button.pack()

# Nút chức năng
buttons = []
buttons.append(tk.Button(canvas, text="Roll right", command=rotate_image))
buttons.append(tk.Button(canvas, text="Roll left", command=rotate_image_left))
buttons.append(tk.Button(canvas, text="Color", command=choose_color))
buttons.append(tk.Button(canvas, text="Chức năng 3"))
buttons.append(tk.Button(canvas, text="Chức năng 4"))
buttons.append(tk.Button(canvas, text="Chức năng 5"))
buttons.append(tk.Button(canvas, text="Reset", command=reset_image))
buttons.append(tk.Button(canvas, text="Save", command=save_image))


image_path = None
original_image = None
current_image = None
tk_image = None

root.mainloop()