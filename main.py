from customtkinter import *

window = CTk()
window.geometry("400x400")
window.wm_resizable(False, False)

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
        for widget in frame.winfo_children():
            widget.destroy()
        frame.destroy()

    frame = CTkScrollableFrame(main, width=380, height=400)
    frame.place(x=0, y=0)

    for i in range(number_of_ins):
        box = resource_box(frame, i + 1)
        box.grid(column=0, row=i * 2, padx=10, pady=(5, 0))  # Box nằm ở hàng chẵn

        # Separator nằm ở hàng lẻ ngay dưới box
        sep = CTkFrame(frame, height=1, width=320, fg_color="gray")
        sep.grid(column=0, row=i * 2 + 1, padx=10, pady=(2, 5), sticky="ew")

    enter = CTkButton(frame, text="Dump to zip file...", command=_on_enter_pressed)
    enter.grid(column=0, row=number_of_ins * 2, pady=10)

def resource_box(parent, ID) -> CTkFrame:
    nframe = CTkFrame(parent, width=340, height=80, corner_radius=10, border_width=0)
    nframe.grid_propagate(False)

    ID_label = CTkLabel(nframe, text=f"ID: {ID}", font=("Arial", 13))
    ID_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 2))

    path_label = CTkLabel(nframe, text="Path: (no file)", font=("Arial", 12), text_color="gray")
    path_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))

    return nframe

main_menu(window)
window.mainloop()
