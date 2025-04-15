from customtkinter import *


window = CTk()
window.geometry("400x400")
window.wm_resizable(False,False)

def main_menu(main):
    def on_button_pressed():
        a = inp.get()
        try:
            int(a)
        except:
            return
        

        #not error:(data is int):
        label.grid_forget()
        inp.grid_forget()
        but.grid_forget()
        _after_main(main,int(a))

        
    label = CTkLabel(main,text = "Enter the number of picture:" )
    label.grid(column = 1,row = 1)
    
    inp = CTkEntry(main,width = 100)
    inp.grid(column=2,row=1)

    but = CTkButton(main,text = "Enter",command = on_button_pressed)
    but.grid(column = 2,row = 2)

def _after_main(main,number_of_ins):
    lst = []
    frame = CTkScrollableFrame(main,width = 380,height=400)
    frame.place(x=0,y=0)

    for i in range(number_of_ins):
        lab = CTkLabel(frame,text = "Free fire")
        lst.append(lab)
        lab.grid(column = 1,row = i+1)
    enter = CTkButton(frame,text = "Dump to zip file...")
    enter.grid(column = 1, row=i+2)


main_menu(window)
window.mainloop()