import os
import mimetypes
from tkinter import Tk, Label, Button, filedialog, messagebox, ttk, Frame, Listbox, END
from PIL import Image
from PIL import ImageTk
import threading
import webbrowser

from optimizer import start_optimization

def select_file(progress_bar, optimize_button, file_label, progress_frame, output_listbox):
    input_path = filedialog.askopenfilename()
    if input_path:
        file_label.config(text=f"Selected file: {os.path.basename(input_path)}")
        optimize_button.config(state="normal")
        optimize_button.config(command=lambda: start_optimization(input_path, progress_bar, file_label, progress_frame, output_listbox))

def open_optimized_folder():
    optimized_folder = os.path.abspath("Optimized Files")
    webbrowser.open(f"file://{optimized_folder}")

def create_gui():
    root = Tk()
    root.title("OptiFile - File Optimizer")

    app_name_label = ttk.Label(root, text="OptiFile", font=("Helvetica", 80, "bold"), foreground="#0000FF", relief="raised")

    app_name_label.pack(pady=10)

    created_by_label = ttk.Label(root, text="Created by arp4zrex", font=("Helvetica", 9, "bold"), foreground="black")

    created_by_label.pack(pady=5)

    original_logo = Image.open("logo.png")
    resized_logo = original_logo.resize((300, 300))
    logo = ImageTk.PhotoImage(resized_logo)
    logo_label = Label(root, image=logo)
    logo_label.image = logo  
    logo_label.pack()

    label = Label(root, text="Select a file to optimize:")
    label.pack(pady=10)

    select_button = Button(root, text="Select File", command=lambda: select_file(progress_bar, optimize_button, file_label, progress_frame, output_listbox))
    select_button.pack(pady=5)

    optimize_button = Button(root, text="Optimize File", state="disabled")
    optimize_button.pack(pady=5)

    file_label = Label(root, text="")
    file_label.pack(pady=10)

    progress_frame = Frame(root)
    progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate', length=200)
    progress_bar.pack(fill='x')
    progress_frame.pack_forget()

    output_label = Label(root, text="Optimized Files:")
    output_label.pack(pady=10)

    output_listbox = Listbox(root, width=80, height=10)
    output_listbox.pack(pady=5)

    open_folder_button = Button(root, text="Open Optimized Folder", command=open_optimized_folder)
    open_folder_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
