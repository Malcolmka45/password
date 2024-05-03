import random
from tkinter import messagebox, Tk, Label, Entry, Button, StringVar

# Define the character string globally
character_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

def generate_password():
    try:
        repeat = int(repeat_entry.get())
        length = int(length_entry.get())
        
        if repeat == 1:
            password = random.sample(character_string, length)
        else:
            password = random.choices(character_string, k=length)
        
        password = ''.join(password)
        password_v.set("Created Password: " + password)
        
    except ValueError:
        messagebox.showerror("Error", "Please key in the required inputs")

# Create the main window
password_gen = Tk()
password_gen.geometry("350x200")
password_gen.title("PythonGeeks Password Generator")

# Title of the app
title_label = Label(password_gen, text="PythonGeeks Password Generator", font=('Ubuntu Mono', 12))
title_label.pack()

# Read length
length_label = Label(password_gen, text="Enter length of password: ")
length_label.place(x=20, y=30)
length_entry = Entry(password_gen, width=3)
length_entry.place(x=190, y=30)

# Read repetition
repeat_label = Label(password_gen, text="Repetition? 1: no repetition, 2: otherwise: ")
repeat_label.place(x=20, y=60)
repeat_entry = Entry(password_gen, width=3)
repeat_entry.place(x=300, y=60)

# Generate password
password_v = StringVar(password_gen)
password_label = Entry(password_gen, bd=0, bg="gray85", textvariable=password_v, state="readonly")
password_label.place(x=10, y=140, height=50, width=320)
password_button = Button(password_gen, text="Generate Password", command=generate_password)
password_button.place(x=100, y=100)

# Run the main loop
password_gen.mainloop()
