from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def random_pass():
    pass_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*']

    s_letter = [random.choice(letters) for _ in range(4)]
    s_num = [random.choice(numbers) for _ in range(4)]
    s_sym = [random.choice(symbols) for _ in range(4)]
    s = s_sym + s_num + s_letter
    random.shuffle(s)
    password = "".join(s)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


#  --------------------------- FIND PASSWORD ------------------------------- #

def find_pass():
    with open("data.json", "r") as f:
        data_file = json.load(f)
        for key in data_file:
            if key == website_entry.get():
                messagebox.showinfo(title="Data File Found", message=f"Email: {data_file[key]['email']}\nPassword: {data_file[key]['password']} \n " )
                return
        messagebox.showinfo(title="No Data File Found", message="No details for the website exists")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_pass():
    new_data = {
        website_entry.get(): {
            "email": username_entry.get(),
            "password": pass_entry.get()
        }
    }
    if len(username_entry.get()) == 0 or len(pass_entry.get()) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")

    else:
        is_ok = messagebox.askokcancel(title=website_entry.get(),
                                       message=f"These are the details entered: \nEmail: {username_entry.get()}\n Password: {pass_entry.get()} \n Is it okay to save?   ")

        if is_ok:
            try:
                with open("data.json", mode="r") as f:
                    data = json.load(f)

            except FileNotFoundError:
                with open("data.json", "w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as f:
                    json.dump(data, f, indent=4)

            finally:
                website_entry.delete(0, END)
                pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# LABELS
website_label = Label(text="Website:", bg="white", font=("Arial", 12))
website_label.grid(row=1, column=0)
username_label = Label(text="Email/Username:", bg="white", font=("Arial", 12))
username_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg="white", font=("Arial", 12))
password_label.grid(row=3, column=0)

# ENTRY
website_entry = Entry(width=17)
website_entry.grid(row=1, column=1)
website_entry.focus()
username_entry = Entry(width=35)
username_entry.insert(0, "aditya@gmail.com")
username_entry.grid(row=2, column=1, columnspan=2)
pass_entry = Entry(text="", width=17)
pass_entry.grid(row=3, column=1)

# BUTTON
gen_pass_button = Button(text='Generate Password', font=("Arial", 10), bg="white", command=random_pass)
gen_pass_button.grid(row=3, column=2)
add_button = Button(text='Add', width=36, font=("Arial", 10), bg="white", command=save_pass)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", font=("Arial", 10), width=13, bg="white", command=find_pass)
search_button.grid(row=1, column=2)
window.mainloop()
