import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess

BASE_DIR = r'F:/codes/cloud master/'

# Initialize lists to store file paths and states (for checkboxes)
uploaded_excel_files = []
uploaded_templates = []
excel_selected = []  # List of boolean values representing checkbox states
template_selected = []

def upload_excel():
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        base_path = os.path.join(BASE_DIR, 'data/')
        os.makedirs(base_path, exist_ok=True)
        new_file_path = os.path.join(base_path, os.path.basename(file_path))
        with open(file_path, 'rb') as f_src:
            with open(new_file_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
        uploaded_excel_files.append(new_file_path)
        excel_selected.append(tk.BooleanVar())  # Add a BooleanVar for checkbox state
        update_excel_list()

def upload_template():
    template_path = filedialog.askopenfilename(title="Select Template File", filetypes=[("HTML Files", "*.html")])
    if template_path:
        base_path = os.path.join(BASE_DIR, 'templates/')
        os.makedirs(base_path, exist_ok=True)
        new_file_path = os.path.join(base_path, os.path.basename(template_path))
        with open(template_path, 'rb') as f_src:
            with open(new_file_path, 'wb') as f_dst:
                f_dst.write(f_src.read())
        uploaded_templates.append(new_file_path)
        template_selected.append(tk.BooleanVar())  # Add a BooleanVar for checkbox state
        update_template_list()

def update_excel_list():
    for widget in excel_frame.winfo_children():
        widget.destroy()  # Clear the listbox
    for i, file in enumerate(uploaded_excel_files):
        chk = ttk.Checkbutton(excel_frame, text=os.path.basename(file), variable=excel_selected[i])
        chk.pack(anchor='w')

def update_template_list():
    for widget in template_frame.winfo_children():
        widget.destroy()  # Clear the listbox
    for i, file in enumerate(uploaded_templates):
        chk = ttk.Checkbutton(template_frame, text=os.path.basename(file), variable=template_selected[i])
        chk.pack(anchor='w')

def send_emails():
    # Get selected Excel file and template
    selected_excel = [uploaded_excel_files[i] for i, var in enumerate(excel_selected) if var.get()]
    selected_template = [uploaded_templates[i] for i, var in enumerate(template_selected) if var.get()]
    
    if not selected_excel or not selected_template:
        messagebox.showerror("Error", "Please select an Excel file and a template.")
        return

    print(f'email passed {selected_excel} template passed {selected_template}')
    # Call the send_email.py script with the selected files
    result = subprocess.run(['python',  os.path.join(BASE_DIR, 'scripts/send_emails.py'), selected_excel[0], selected_template[0]], capture_output=True, text=True)

    if result.returncode == 0:
        messagebox.showinfo("Success", "Emails sent successfully!")
    else:
        messagebox.showerror("Error", result.stderr)

# GUI layout
root = tk.Tk()
root.title("Cloud Master - Bulk Email Sender")
root.geometry("800x600")

# Excel frame for checkboxes
excel_frame = tk.Frame(root)
excel_frame.pack(pady=10)
upload_excel_btn = tk.Button(root, text="Upload Excel File", command=upload_excel)
upload_excel_btn.pack(pady=10)

# Template frame for checkboxes
template_frame = tk.Frame(root)
template_frame.pack(pady=10)
upload_template_btn = tk.Button(root, text="Upload HTML Template", command=upload_template)
upload_template_btn.pack(pady=10)

send_btn = tk.Button(root, text="Send Emails", command=send_emails)
send_btn.pack(pady=20)

root.mainloop()
