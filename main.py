import json
import string
from random import choice
from tkinter import END, Canvas, PhotoImage, messagebox

from customtkinter import (  # type: ignore
    CTk,
    CTkButton,
    CTkEntry,
    CTkLabel,
    CTkSlider,
    set_appearance_mode,
    set_default_color_theme,
)


# ---------- Generate Password ------------
def generate_password() -> None:
    global value
    password_entry.delete(0, END)
    # Define the character sets
    lowercase_letters: str = string.ascii_lowercase
    uppercase_letters: str = string.ascii_uppercase
    digits: str = string.digits
    symbols: str = string.punctuation

    # Combine all character sets
    all_characters: str = lowercase_letters + uppercase_letters + digits + symbols

    # Generate a password with random characters
    password: str = "".join(choice(all_characters) for _ in range(value))
    password_entry.insert(0, password)


# ---------- Save Logic ------------
def save() -> None:
    web: str = website_entry.get()
    email: str = email_entry.get()
    pass_: str = password_entry.get()

    new_data: dict[str, dict[str, str]] = {web: {"email": email, "password": pass_}}

    if len(web) < 3 or len(email) < 3 or len(pass_) < 8:
        messagebox.showinfo(title="Information", message="Data is short.")
    # Rest of the code...
    else:
        try:
            with open("passwords.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------- UI ------------
value: int = 12


def slider_value(value_: int) -> None:
    global value
    value = int(value_)
    slider_num.configure(text=value)


root: CTk = CTk()
root.title("Password Manager")
root.config(padx=20, pady=20)
set_default_color_theme("dark-blue")
set_appearance_mode("dark")

canvas: Canvas = Canvas(master=root, width=200, height=200)
canvas.config(bg=root["bg"], highlightthickness=0)  # using root bg color
image_path: PhotoImage = PhotoImage(file="pass.png")
canvas.create_image(100, 100, image=image_path)
canvas.grid(column=1, row=0)

website_label: CTkLabel = CTkLabel(root, text="Website:")
website_label.grid(column=0, row=1, sticky="e")
website_entry: CTkEntry = CTkEntry(root, height=15, width=300)
website_entry.grid(column=1, row=1, columnspan=2, padx=20, sticky="w")
website_entry.focus()

email_label: CTkLabel = CTkLabel(root, text="Email/Username:")
email_label.grid(column=0, row=2, sticky="e")
email_entry: CTkEntry = CTkEntry(root, height=15, width=300)
email_entry.grid(column=1, row=2, columnspan=2, padx=20, sticky="w")

password_label: CTkLabel = CTkLabel(root, text="Password:")
password_label.grid(column=0, row=3, sticky="e")
password_entry: CTkEntry = CTkEntry(root, height=15, width=200)
password_entry.grid(column=1, row=3, padx=(20, 0), sticky="w")

generate_button: CTkButton = CTkButton(
    root, text="Generate", width=80, height=15, command=generate_password
)
generate_button.grid(column=2, row=3, padx=(0, 0), sticky="w")

slider_label: CTkLabel = CTkLabel(root, text="Password Length:")
slider_label.grid(column=0, row=4, sticky="e")
slider: CTkSlider = CTkSlider(
    root, from_=8, to=25, orientation="horizontal", width=200, command=slider_value
)
slider.grid(column=1, row=4, padx=(20, 0), sticky="w")
slider_num: CTkLabel = CTkLabel(root, text=value)
slider_num.grid(column=2, row=4, padx=(20, 0), sticky="w")

add_button: CTkButton = CTkButton(root, text="Add", height=15, width=300, command=save)
add_button.grid(column=1, row=5, padx=20, pady=5, sticky="w", columnspan=2)

root.resizable(False, False)
root.mainloop()
