import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import PyPDF2
import merge
import split
import compress

def rotate(logo_label, button1, button2, button3, button4, root):
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

    # rotate button
    rotate_button = tk.Button(root, text='Rotate (cw) at:', command=lambda:magic(files, home_dir, text_box, rotate_at_combobox), bg='#ff474a', fg='white', font='Raleway', height=3)
    rotate_button.grid(column=0, row=1, sticky='ew')

    # rotate at combobox
    rotate_at_combobox = ttk.Combobox(root, values=[90, 180, 270])
    rotate_at_combobox.grid(column=1, row=1)

    # home button
    home_button = tk.Button(root, text='Home', command=lambda:home(text_box, add_file_button, rotate_button, home_button, rotate_at_combobox, logo_label, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    home_button.grid(column=0, row=2, sticky='ew')
    
    # add file(s) button
    add_file_button = tk.Button(root, text='Add File(s)', command=lambda:add_files(root, text_box, files, home_dir), bg='#ff474a', fg='white', font='Raleway', height=3)
    add_file_button.grid(column=1, row=2, sticky='ew')

def add_files(root, text_box, files, home_dir):
    file = askopenfilename(parent=root, title='Add a file', filetypes=[('PDF file', '*.pdf')], initialdir=home_dir)
    if file:
        if len(files) == 0:
            text_box.delete('1.0', 'end')
            text_box.insert('1.0', 'File(s) to rotate (clockwise):\n\n')
        files.append(file)
        text_box.insert('end', f'{len(files)}. {file}\n\n')

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
    split_button = tk.Button(root, text='Split', command=lambda:split.split(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    split_button.grid(column=1, row=1, sticky='ew')
    rotate_button = tk.Button(root, text='Rotate', command=lambda:rotate(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    rotate_button.grid(column=0, row=2, sticky='ew')
    compress_button = tk.Button(root, text='Compress', command=lambda:compress.compress(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    compress_button.grid(column=1, row=2, sticky='ew')

def magic(files, home_dir, text_box, rotate_at_combobox):
    if len(files) != 0:
        try:
            angle = int(rotate_at_combobox.get())
            for number, file in enumerate(files):
                input_file = PyPDF2.PdfFileReader(file)
                output_file = PyPDF2.PdfFileWriter()
                for page in range(input_file.numPages):
                    page = input_file.getPage(page)
                    page.rotateClockwise(angle)
                    output_file.addPage(page)
                stream = open(f'{home_dir}{os.sep}file_{number+1}_{angle}_rotated.pdf', 'wb')
                output_file.write(stream)
            text_box.delete('1.0', 'end')
            text_box.insert('1.0', 'PDF files has been rotated successfully!\n')
            text_box.insert('end', 'The files are saved in:\n')
            for number, file in enumerate(files):
                text_box.insert('end', f'{number+1}. {home_dir}{os.sep}file_{number+1}_{angle}_rotated.pdf\n')
            files.clear()
        except:
            text_box.insert('end', 'Error occurred!')
    else:
        text_box.delete('1.0', 'end')
        text_box.insert('end', 'No file to rotate. Please select one.')