import itertools
import string
import tkinter as tk
from tkinter import messagebox

def load_dictionary(file_path):
    """Load the dictionary from a text file."""
    try:
        with open(file_path, 'r') as file:
            dictionary = [line.strip() for line in file]
        return dictionary
    except FileNotFoundError:
        messagebox.showerror("Error", "Dictionary file not found!")
        return []

def dictionary_attack(username, password, dictionary):
    print(f"Attempting dictionary attack for user: {username}")
    for word in dictionary:
        if word == password:
            return True, word
    return False, None

def brute_force_attack(password):
    print("Dictionary attack failed. Starting brute-force attack...")
    chars = string.ascii_letters  # A-Z, a-z
    for attempt in itertools.product(chars, repeat=5):
        attempt_password = ''.join(attempt)
        if attempt_password == password:
            return True, attempt_password
    return False, None

def start_attack():
    username = username_entry.get()
    if not username:
        messagebox.showerror("Error", "Please enter a username.")
        return
    
    correct_password = "mohab"  # Hardcoded correct password
    
    # Load dictionary from file
    dictionary = load_dictionary("10-million-password-list-top-1000000.txt")
    if not dictionary:
        return
    
    success, found_password = dictionary_attack(username, correct_password, dictionary)
    if success:
        messagebox.showinfo("Success", f"Dictionary Attack Successful! Password: {found_password}")
        return
    
    success, found_password = brute_force_attack(correct_password)
    if success:
        messagebox.showinfo("Success", f"Brute Force Attack Successful! Password: {found_password}")
    else:
        messagebox.showerror("Failure", "Brute Force Attack Failed.")

# GUI Setup
root = tk.Tk()
root.title("Password Cracker")
root.geometry("400x300")  # Set window size to 400x300

tk.Label(root, text="Enter Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Button(root, text="Start Attack", command=start_attack).pack()

root.mainloop()