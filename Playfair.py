import tkinter as tk
from tkinter import messagebox

def generate_key_square(key):
    key = key.replace(" ", "").upper()
    key_square = ""
    for char in key:
        if char not in key_square:
            key_square += char
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in key_square:
            key_square += char
    return key_square

def prepare_input(text):
    text = text.upper().replace(" ", "").replace("J", "I")
    prepared_text = ""
    i = 0
    while i < len(text):
        prepared_text += text[i]
        if i < len(text) - 1:
            if text[i] == text[i + 1]:
                prepared_text += "X"
                i -= 1
        i += 1
    if len(prepared_text) % 2 != 0:
        prepared_text += "X"
    return prepared_text

def find_position(key_square, letter):
    row = 0
    col = 0
    for i in range(5):
        for j in range(5):
            if key_square[i*5 + j] == letter:
                row = i
                col = j
                break
    return row, col

def encrypt(plaintext, key):
    key_square = generate_key_square(key)
    prepared_text = prepare_input(plaintext)
    ciphertext = ""
    for i in range(0, len(prepared_text), 2):
        char1 = prepared_text[i]
        char2 = prepared_text[i + 1]
        row1, col1 = find_position(key_square, char1)
        row2, col2 = find_position(key_square, char2)
        if row1 == row2:
            ciphertext += key_square[row1*5 + (col1 + 1) % 5]
            ciphertext += key_square[row2*5 + (col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += key_square[((row1 + 1) % 5)*5 + col1]
            ciphertext += key_square[((row2 + 1) % 5)*5 + col2]
        else:
            ciphertext += key_square[row1*5 + col2]
            ciphertext += key_square[row2*5 + col1]
    return ciphertext

def decrypt(ciphertext, key):
    key_square = generate_key_square(key)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1]
        row1, col1 = find_position(key_square, char1)
        row2, col2 = find_position(key_square, char2)
        if row1 == row2:
            plaintext += key_square[row1*5 + (col1 - 1) % 5]
            plaintext += key_square[row2*5 + (col2 - 1) % 5]
        elif col1 == col2:
            plaintext += key_square[((row1 - 1) % 5)*5 + col1]
            plaintext += key_square[((row2 - 1) % 5)*5 + col2]
        else:
            plaintext += key_square[row1*5 + col2]
            plaintext += key_square[row2*5 + col1]
    return plaintext

def encrypt_text():
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if len(plaintext) == 0 or len(key) == 0:
        messagebox.showerror("Error", "Vui lòng nhập văn bản và khóa.")
        return
    ciphertext = encrypt(plaintext, key)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ciphertext)

def decrypt_text():
    ciphertext = ciphertext_entry.get()
    key = key_entry.get()
    if len(ciphertext) == 0 or len(key) == 0:
        messagebox.showerror("Error", "Vui lòng nhập văn bản đã mã hóa và khóa.")
        return
    plaintext = decrypt(ciphertext, key)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, plaintext)

# Tạo giao diện
root = tk.Tk()
root.title("Playfair Cipher")

plaintext_label = tk.Label(root, text="Văn bản:")
plaintext_label.grid(row=0, column=0, padx=5, pady=5)
plaintext_entry = tk.Entry(root, width=30)
plaintext_entry.grid(row=0, column=1, padx=5, pady=5)

key_label = tk.Label(root, text="Khóa:")
key_label.grid(row=1, column=0, padx=5, pady=5)
key_entry = tk.Entry(root, width=30)
key_entry.grid(row=1, column=1, padx=5, pady=5)

encrypt_button = tk.Button(root, text="Mã hóa", command=encrypt_text)
encrypt_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

ciphertext_label = tk.Label(root, text="Văn bản đã mã hóa:")
ciphertext_label.grid(row=3, column=0, padx=5, pady=5)
ciphertext_entry = tk.Entry(root, width=30)
ciphertext_entry.grid(row=3, column=1, padx=5, pady=5)

decrypt_button = tk.Button(root, text="Giải mã", command=decrypt_text)
decrypt_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

result_label = tk.Label(root, text="Kết quả:")
result_label.grid(row=5, column=0, padx=5, pady=5)
result_text = tk.Text(root, width=30, height=4)
result_text.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()