from tkinter import *
from PIL import Image
from random import *
import pyperclip
from tkinter import messagebox
import json

FONT = ('Helvetica', 10, 'bold')


# *********************** GENERATE PASSWORD **************************
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!' '#', '$', '%', '&', '(', ')', '*', '+', '/', '<', '>', '?', '@', '[', ']', '_', '{', '}', '~']

    random_letters = choices(letters, k=6)
    random_numbers = choices(numbers, k=3)
    random_symbols = choices(symbols, k=1)

    random_password = random_letters + random_numbers + random_symbols
    shuffle(random_password)

    password = "".join(random_password)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# *********************** SHOW PASSWORD *****************************
def show_password():
    if var1.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


# ******************************** SAVE PASSWORD **************************************

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title='Error', message="Please don't leave any field empty.")
    else:
        if messagebox.askokcancel(title='Alert!', message=f'Website: {website}\nEmail: {email}\nPassword: {password}\n'
                                                          f'Is it okay to save?') == 1:
            try:
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open('data.json', 'w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open('data.json', 'w') as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo(title='Success', message='Password saved and copied to clipboard.')


# ********************************** FIND PASSWORD *************************************
def find():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message='No data file found.')
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f'{website}', message=f'Email: {email}\nPassword: {password}')
        else:
            messagebox.showinfo(title='Error', message=f'No details for {website} exist.')


# ********************************** UI DESIGN ******************************************
window = Tk()
window.title('Password Manager')
window.minsize(width=700, height=500)
window.maxsize(width=700, height=500)
window.config(bg='black', pady=10, padx=10)

canvas = Canvas(width=200, height=200, background='black', highlightthickness=0)
img = Image.open('logo.png')
resized_img = img.resize((200, 200))
resized_img.save('logo.png')
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=2, pady=40)

website_label = Label(text='Website: ',
                      foreground='white',
                      background='black',
                      font=FONT)
website_label.grid(row=1, column=0)

website_entry = Entry(background='black',
                      foreground='white',
                      highlightcolor='white',
                      cursor='xterm',
                      insertbackground="white",
                      width=50
                      )
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2)

email_label = Label(text='Email/Username: ',
                    foreground='white',
                    background='black',
                    font=FONT)
email_label.grid(row=2, column=0)

email_entry = Entry(background='black',
                    foreground='white',
                    highlightcolor='white',
                    cursor='xterm',
                    insertbackground="white",
                    width=50)
email_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text='Password: ', foreground='white', background='black', font=FONT)
password_label.grid(row=3, column=0)

password_entry = Entry(background='black', foreground='white', highlightcolor='white',
                       cursor='xterm',
                       insertbackground="white",
                       show='*',
                       width=50)
password_entry.grid(row=3, column=1, columnspan=2)
var1 = IntVar()
show_button = Checkbutton(text='Show Password',
                          variable=var1,
                          offvalue=0,
                          onvalue=1,
                          command=show_password,
                          bg='black',
                          fg='white',
                          selectcolor='black',
                          )
show_button.grid(row=4, column=0)

find_password = Button(text='Find Password',
                       bg='black',
                       fg='white',
                       width=15,
                       command=find)
find_password.grid(row=1, column=3)

generate_password = Button(text='Generate Password',
                           bg='black',
                           fg='white',
                           width=15,
                           command=generate_password)
generate_password.grid(row=2, column=3)

add_password = Button(text='Add Password',
                      bg='black',
                      fg='white',
                      width=15,
                      command=save_password)
add_password.grid(row=3, column=3)

footer_label = Label(text='©Created by Manish Yadav',
                     bg='black',
                     fg='white',
                     pady=20)
footer_label.grid(row=5, column=2)

window.mainloop()
