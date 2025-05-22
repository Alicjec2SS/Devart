import os
import sys
import zipfile
import time
from tkinter import filedialog
from PIL import Image
from customtkinter import *
from CTkMessagebox import *

window = CTk()
window.geometry("400x500")
window.wm_resizable(False, False)
set_appearance_mode("Dark")

image_data_list = []

def main_menu(main):
    def on_button_pressed():
        a = inp.get()
        try:
            num = int(a)
        except:
            return

        # Nếu đúng là số:
        label.grid_forget()
        inp.grid_forget()
        but.grid_forget()
        _after_main(main, num)

    label = CTkLabel(main, text="Enter the number of pictures:")
    label.grid(column=1, row=1)

    inp = CTkEntry(main, width=100)
    inp.grid(column=2, row=1)

    but = CTkButton(main, text="Enter", command=on_button_pressed)
    but.grid(column=2, row=2)

def _after_main(main, number_of_ins):
    def _on_enter_pressed():
        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if not save_path:
            return

        with zipfile.ZipFile(save_path, "w") as zipf:
            for data in image_data_list:
                if data["path"] is not None and data["id"] is not None:
                    try:
                        ext = os.path.splitext(data["path"])[1]
                        target_name = f"{data['id']}{ext}"
                        zipf.write(data["path"], target_name)
                    except Exception as e:
                        print(f"Error adding {data['path']}: {e}")

        CTkLabel(main, text="Done!").place(x=160, y=470)
        CTkMessagebox(window,title = "Done",message="done")
        time.sleep(2)
        sys.exit()



    frame = CTkScrollableFrame(main, width=380, height=460)
    frame.place(x=10, y=10)

    for i in range(number_of_ins):
        image_data_list.append({"id": str(i + 1), "path": None})
        box = resource_box(frame, i + 1)
        box.grid(column=0, row=i * 2, padx=10, pady=(5, 0))

        sep = CTkFrame(frame, height=1, width=320, fg_color="gray")
        sep.grid(column=0, row=i * 2 + 1, padx=10, pady=(2, 5), sticky="ew")

    enter = CTkButton(frame, text="Dump to zip file...", command=_on_enter_pressed)
    enter.grid(column=0, row=number_of_ins * 2, pady=10)

def resource_box(parent, ID) -> CTkFrame:
    nframe = CTkFrame(parent, width=340, height=100, corner_radius=10)
    nframe.grid_propagate(False)

    ID_label = CTkLabel(nframe, text=f"ID: {ID}", font=("Arial", 13))
    ID_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 2))

    path_label = CTkLabel(nframe, text="Path: (no file)", font=("Arial", 12), text_color="gray")
    path_label.grid(row=1, column=0, sticky="w", padx=15)

    img_label = CTkLabel(nframe, text="(No image)")
    img_label.grid(row=0, column=1, rowspan=2, padx=10, pady=5)

    def select_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if file_path:
            try:
                pil_image = Image.open(file_path)
                pil_image.thumbnail((100, 100))  # Resize giữ tỷ lệ

                ctk_img = CTkImage(light_image=pil_image, size=(100, 100))
                img_label.configure(image=ctk_img, text="")
                img_label.image = ctk_img

                path_label.configure(text=os.path.basename(file_path), text_color="white")
                image_data_list[ID - 1]["path"] = file_path
            except Exception as e:
                print(f"Lỗi khi mở ảnh: {e}")

    pick_btn = CTkButton(nframe, text="Select Image", width=100, command=select_image)
    pick_btn.grid(row=2, column=0, padx=15, pady=5, sticky="w")

    return nframe

main_menu(window)
window.mainloop()
