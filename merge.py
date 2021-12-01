import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import PyPDF2
import split
import rotate
import compress

def merge(logo_label, button1, button2, button3, button4, root):
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

    # clear button
    clear_button = tk.Button(root, text='Clear', command=lambda:clear(files, text_box), bg='#ff474a', fg='white', font='Raleway', height=3)
    clear_button.grid(column=0, row=1, sticky='ew')
    
    # add file(s) button
    add_file_button = tk.Button(root, text='Add File(s)', command=lambda:add_files(root, text_box, files, home_dir), bg='#ff474a', fg='white', font='Raleway', height=3)
    add_file_button.grid(column=1, row=1, sticky='ew')

    # home button
    home_button = tk.Button(root, text='Home', command=lambda:home(text_box, add_file_button, merge_button, home_button, logo_label, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    home_button.grid(column=0, row=2, sticky='ew')

    # merge button
    merge_button = tk.Button(root, text='Merge', command=lambda:magic(files, home_dir, text_box), bg='#ff474a', fg='white', font='Raleway', height=3)
    merge_button.grid(column=1, row=2, sticky='ew')

def clear(files, text_box):
    files.clear()
    text_box.delete('1.0', 'end')

def add_files(root, text_box, files, home_dir):
    file = askopenfilename(parent=root, title='Add a file', filetypes=[('PDF file', '*.pdf')], initialdir=home_dir)
    if file:
        if len(files) == 0:
            text_box.delete('1.0', 'end')
            text_box.insert('1.0', 'File(s) to merge:\n\n')
        files.append(file)
        text_box.insert('end', f'{len(files)}. {file}\n\n')

def home(text_box, button1, button2, button3, logo_label, root):
    # clear window
    text_box.grid_remove()
    button1.grid_remove()
    button2.grid_remove()
    button3.grid_remove()

    # restore logo_label
    logo_label.grid(columnspan=2, row=0)

    # restore buttons
    merge_button = tk.Button(root, text='Merge', command=lambda:merge(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    merge_button.grid(column=0, row=1, sticky='ew')
    split_button = tk.Button(root, text='Split', command=lambda:split.split(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    split_button.grid(column=1, row=1, sticky='ew')
    rotate_button = tk.Button(root, text='Rotate', command=lambda:rotate.rotate(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    rotate_button.grid(column=0, row=2, sticky='ew')
    compress_button = tk.Button(root, text='Compress', command=lambda:compress.compress(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    compress_button.grid(column=1, row=2, sticky='ew')

def magic(files, home_dir, text_box):
    if len(files) > 1:
        try:
            merge_file = PyPDF2.PdfFileMerger()
            for file in files:
                merge_file.append(PyPDF2.PdfFileReader(file, 'rb'))
            merge_file.write(f'{home_dir}{os.sep}merged.pdf')
            text_box.delete('1.0', 'end')
            text_box.insert('1.0', 'PDF files has been merged successfully!\n')
            text_box.insert('end', f'The file is saved in {home_dir}{os.sep}merged.pdf')
            files.clear()
        except:
            text_box.insert('end', 'Error occurred!')
    else:
        text_box.delete('1.0', 'end')
        text_box.insert('end', 'Nothing to merge! Please add more file.')