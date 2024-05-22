import tkinter as tk
import cv2
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFilter

def show_picture():
    global image_path, original_image, current_image, drawing_layer, draw, current_angle
    image_path = filedialog.askopenfilename()
    if image_path:
        original_image = Image.open(image_path)
        current_image = original_image.copy()
        drawing_layer = Image.new("RGBA", original_image.size)
        draw = ImageDraw.Draw(drawing_layer)
        current_angle = 0
        display_image(current_image)

def display_image(image):
    global tk_image, img_x, img_y, img_width, img_height
    combined_image = Image.alpha_composite(image.convert("RGBA"), drawing_layer)
    tk_image = ImageTk.PhotoImage(combined_image)

    canvas.delete("all")  # Xóa tất cả các vật thể trước khi vẽ hình ảnh mới

    # Tính toán tọa độ để hiển thị ảnh ở trung tâm canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    img_width = tk_image.width()
    img_height = tk_image.height()
    img_x = (canvas_width - img_width) // 2
    img_y = (canvas_height - img_height) // 2

    canvas.create_image(img_x, img_y, anchor="nw", image=tk_image)
    canvas.image = tk_image  # Giữ tham chiếu để hình ảnh không bị hủy bỏ

    # Thêm các nút vào hình ảnh
    num_buttons = len(buttons)
    button_height = 30
    spacing = 10
    total_height = num_buttons * button_height + (num_buttons - 1) * spacing
    start_y = (canvas_height - total_height) // 2

    for i, button in enumerate(buttons):
        button_y = start_y + i * (button_height + spacing)
        canvas.create_window(10, button_y, anchor="nw", window=button, width=100, height=button_height)

def rotate_image():
    global current_image, drawing_layer, draw, current_angle
    if current_image:
        current_angle = (current_angle + 90) % 360
        current_image = current_image.rotate(90, expand=True)
        drawing_layer = drawing_layer.rotate(90, expand=True)
        draw = ImageDraw.Draw(drawing_layer)
        display_image(current_image)

def rotate_image_left():
    global current_image, drawing_layer, draw, current_angle
    if current_image:
        current_angle = (current_angle - 90) % 360
        current_image = current_image.rotate(-90, expand=True)
        drawing_layer = drawing_layer.rotate(-90, expand=True)
        draw = ImageDraw.Draw(drawing_layer)
        display_image(current_image)

def choose_color():
    global pen_color
    color = colorchooser.askcolor()[1]
    if color:
        pen_color = color

def apply_color_to_image():
    global current_image, drawing_layer, draw, current_angle
    color = colorchooser.askcolor()[1]
    if color and original_image:
        grayscale_image = original_image.convert("L")
        color_image = Image.new("RGB", original_image.size, color)
        colored_image = ImageEnhance.Color(grayscale_image).enhance(0.0)
        colored_image = Image.blend(colored_image.convert("RGB"), color_image, alpha=0.5)
        colored_image = colored_image.convert("RGBA")
        # Áp dụng góc xoay hiện tại
        colored_image = colored_image.rotate(current_angle, expand=True)
        current_image = colored_image
        display_image(current_image)

def apply_filter(filter_type):
    global current_image, drawing_layer, draw, current_angle
    if current_image:
        if filter_type == "BLUR":
            filtered_image = current_image.filter(ImageFilter.BLUR)
        elif filter_type == "SHARPEN":
            filtered_image = current_image.filter(ImageFilter.SHARPEN)
        else:
            return  # Nếu loại bộ lọc không hợp lệ thì không làm gì cả
        # Giữ nguyên góc xoay và các đường vẽ hiện tại
        current_image = filtered_image
        display_image(current_image)

def reset_image():
    global original_image, current_image, drawing_layer, draw, current_angle
    if original_image:
        current_image = original_image.copy()
        drawing_layer = Image.new("RGBA", current_image.size)
        draw = ImageDraw.Draw(drawing_layer)
        current_angle = 0
        display_image(original_image)

def save_image():
    global current_image, drawing_layer
    if current_image:
        combined_image = Image.alpha_composite(current_image.convert("RGBA"), drawing_layer)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            combined_image.save(save_path)

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def draw_on_image(event):
    global last_x, last_y, draw, pen_color, eraser_mode
    x, y = event.x, event.y
    adjusted_x1 = last_x - img_x
    adjusted_y1 = last_y - img_y
    adjusted_x2 = x - img_x
    adjusted_y2 = y - img_y
    if eraser_mode:
        draw.line((adjusted_x1, adjusted_y1, adjusted_x2, adjusted_y2), fill=(0, 0, 0, 0), width=50)  # Increase eraser size
    else:
        draw.line((adjusted_x1, adjusted_y1, adjusted_x2, adjusted_y2), fill=pen_color, width=5)
    last_x, last_y = x, y
    display_image(current_image)

def activate_draw():
    global eraser_mode
    eraser_mode = False
    canvas.config(cursor="pencil")  # Thay đổi con trỏ chuột thành bút
    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw_on_image)

def activate_eraser():
    global eraser_mode
    eraser_mode = True
    canvas.config(cursor="dotbox")  # Thay đổi con trỏ chuột thành cục tẩy
    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw_on_image)

def return_cursor():
    canvas.config(cursor="arrow")  # Trả con trỏ chuột về trạng thái ban đầu
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")

def stop_recording():
    global recording, cap, out
    if recording:
        recording = False
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        record_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        video_window.destroy()

def record_video():
    global recording, cap, out, video_label, video_window, stop_button
    # Initialize VideoCapture with camera ID
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    # Define frame dimensions and frames per second
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30  # Frames per second

    # Create a VideoWriter object to write the video
    save_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi"), ("All files", "*.*")])
    if save_path:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))
        recording = True
        record_button.config(state=tk.DISABLED)

        # Create a new window for video recording
        video_window = tk.Toplevel(root)
        video_window.title("Recording Video")

        # Create a label for displaying the video frames
        video_label = tk.Label(video_window)
        video_label.pack()

        # Create a stop button in the new window
        stop_button = tk.Button(video_window, text="Stop Video", command=stop_recording)
        stop_button.pack()

        # Video writing function
        def write_frame():
            if recording:
                ret, frame = cap.read()
                if ret:
                    # Write frame to the video
                    out.write(frame)

                    # Display the video in the new window
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    img = ImageTk.PhotoImage(image=img)
                    video_label.config(image=img)
                    video_label.image = img

                    # Repeat the function after a certain time interval (milliseconds)
                    video_label.after(10, write_frame)

        # Start recording the video
        write_frame()

root = tk.Tk()
root.title("Image with Buttons")
root.state('zoomed')

canvas = tk.Canvas(root, width=4000, height=600)
canvas.pack(expand=True, fill=tk.BOTH)

open_image_button = tk.Button(root, text="Open Image", command=show_picture)
open_image_button.pack()

exit_image_button = tk.Button(root, text="Exit", command=root.destroy)
exit_image_button.pack()

record_button = tk.Button(root, text="Record Video", command=record_video)
record_button.pack()

# Nút chức năng
buttons = []
buttons.append(tk.Button(canvas, text="Roll right", command=rotate_image))
buttons.append(tk.Button(canvas, text="Roll left", command=rotate_image_left))
buttons.append(tk.Button(canvas, text="Color img", command=apply_color_to_image))
buttons.append(tk.Button(canvas, text="Blur", command=lambda: apply_filter("BLUR")))
buttons.append(tk.Button(canvas, text="Sharpen", command=lambda: apply_filter("SHARPEN")))
buttons.append(tk.Button(canvas, text="Color pen", command=choose_color))
buttons.append(tk.Button(canvas, text="Draw", command=activate_draw))
buttons.append(tk.Button(canvas, text="Erase", command=activate_eraser))
buttons.append(tk.Button(canvas, text="Return", command=return_cursor))
buttons.append(tk.Button(canvas, text="Reset", command=reset_image))
buttons.append(tk.Button(canvas, text="Save", command=save_image))

image_path = None
original_image = None
current_image = None
colored_image = None
tk_image = None
last_x, last_y = None, None
draw = None
pen_color = 'red'  # Màu mặc định của bút
eraser_mode = False  # Trạng thái của cục tẩy
current_angle = 0  # Góc xoay hiện tại của ảnh

# Các biến để lưu trữ vị trí và kích thước của hình ảnh
img_x = img_y = img_width = img_height = 0

# Lớp đệm để vẽ
drawing_layer = None

# Recording flag
recording = False

root.mainloop()
