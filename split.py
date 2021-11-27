import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import PyPDF2
import merge
import rotate
import compress

def split(logo_label, button1, button2, button3, button4, root):
    files = []
    home_dir = os.path.expanduser('~')

    # clear window
    logo_label.grid_remove()
    button1.grid_remove()
    button2.grid_remove()
    button3.grid_remove()
    button4.grid_remove()

    # set up text box
    text_box = tk.Text(root, width=50)
    text_box.grid(columnspan=2, row=0)

    # split button
    split_button = tk.Button(root, text='Split at page:', command=lambda:magic(files, home_dir, text_box, split_at_combobox), bg='#ff474a', fg='white', font='Raleway', height=3)
    split_button.grid(column=0, row=1, sticky='ew')

    # split at combobox
    split_at_combobox = ttk.Combobox(root, values=[])
    split_at_combobox.grid(column=1, row=1)
    
    # home button
    home_button = tk.Button(root, text='Home', command=lambda:home(text_box, choose_file_button, split_button, home_button, split_at_combobox, logo_label, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    home_button.grid(column=0, row=2, sticky='ew')
    
    # choose file button
    choose_file_button = tk.Button(root, text='Choose File', command=lambda:choose_file(root, text_box, home_dir, split_at_combobox, files), bg='#ff474a', fg='white', font='Raleway', height=3)
    choose_file_button.grid(column=1, row=2, sticky='ew')

def choose_file(root, text_box, home_dir, split_at_combobox, files):
    files.clear()
    file = askopenfilename(parent=root, title='Choose a file', filetypes=[('PDF file', '*.pdf')], initialdir=home_dir)
    if file:
        text_box.delete('1.0', 'end')
        text_box.insert('1.0', f'File to split:\n\n{file}\n\n')
        split_at_combobox['values'] = list(range(1, get_page_count(file) + 1))
        files.append(file)

def get_page_count(file):
    reader = PyPDF2.PdfFileReader(open(file, 'rb'))
    return reader.getNumPages()

def home(text_box, button1, button2, button3, combobox, logo_label, root):
    # clear window
    text_box.grid_remove()
    button1.grid_remove()
    button2.grid_remove()
    button3.grid_remove()
    combobox.grid_remove()

    # restore logo_label
    logo_label.grid(columnspan=2, row=0)

    # restore buttons
    merge_button = tk.Button(root, text='Merge', command=lambda:merge.merge(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    merge_button.grid(column=0, row=1, sticky='ew')
    split_button = tk.Button(root, text='Split', command=lambda:split(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    split_button.grid(column=1, row=1, sticky='ew')
    rotate_button = tk.Button(root, text='Rotate', command=lambda:rotate.rotate(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    rotate_button.grid(column=0, row=2, sticky='ew')
    compress_button = tk.Button(root, text='Compress', command=lambda:compress.compress(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    compress_button.grid(column=1, row=2, sticky='ew')

def magic(files, home_dir, text_box, split_at_combobox):
    if files:
        input_file = PyPDF2.PdfFileReader(files[0])
        output_file_1 = PyPDF2.PdfFileWriter()
        output_file_2 = PyPDF2.PdfFileWriter()
        split_at = int(split_at_combobox.get())
        end = int(split_at_combobox['values'][-1])
        for page in range(split_at):
            output_file_1.addPage(input_file.getPage(page))
        stream = open(f'{home_dir}{os.sep}page_1_to_{split_at}.pdf', 'wb')
        output_file_1.write(stream)
        for page in range(split_at, end):
            output_file_2.addPage(input_file.getPage(page))
        stream = open(f'{home_dir}{os.sep}page_{split_at}_to_{end}.pdf', 'wb')
        output_file_2.write(stream)
        text_box.delete('1.0', 'end')
        text_box.insert('1.0', 'PDF files has been splitted successfully!\n')
        text_box.insert('end', 'The files are saved in:\n')
        text_box.insert('end', f'1. {home_dir}{os.sep}page_1_to_{split_at}.pdf\n')
        text_box.insert('end', f'2. {home_dir}{os.sep}page_{split_at}_to_{end}.pdf')
    else:
        text_box.delete('1.0', 'end')
        text_box.insert('1.0', 'No file to split. Please select one.')
