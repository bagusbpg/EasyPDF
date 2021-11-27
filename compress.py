import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import ghostscript as gs
import locale
import merge
import split
import rotate

def compress(logo_label, button1, button2, button3, button4, root):
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

    # compress button
    compress_button = tk.Button(root, text='Compress to:', command=lambda:magic(files, home_dir, text_box, quality_combobox), bg='#ff474a', fg='white', font='Raleway', height=3)
    compress_button.grid(column=0, row=1, sticky='ew')

    # quality combobox
    quality_combobox = ttk.Combobox(root, values=['screen (72 dpi)', 'ebook (150 dpi)', 'printer (300 dpi)', 'prepress (300 dpi +)'])
    quality_combobox.grid(column=1, row=1, sticky='ew')
    
    # home button
    home_button = tk.Button(root, text='Home', command=lambda:home(text_box, choose_file_button, compress_button, home_button, quality_combobox, logo_label, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    home_button.grid(column=0, row=2, sticky='ew')

    # choose file button
    choose_file_button = tk.Button(root, text='Choose File', command=lambda:choose_file(root, text_box, files, home_dir), bg='#ff474a', fg='white', font='Raleway', height=3)
    choose_file_button.grid(column=1, row=2, sticky='ew')

def choose_file(root, text_box, files, home_dir):
    files.clear()
    file = askopenfilename(parent=root, title='Choose a file', filetypes=[('PDF file', '*.pdf')], initialdir=home_dir)
    if file:
        text_box.delete('1.0', 'end')
        text_box.insert('1.0', f'File to compress:\n\n{file}\n\n')
        files.append(file)

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
    rotate_button = tk.Button(root, text='Rotate', command=lambda:rotate.rotate(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    rotate_button.grid(column=0, row=2, sticky='ew')
    compress_button = tk.Button(root, text='Compress', command=lambda:compress(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg='#ff474a', fg='white', font='Raleway', height=3)
    compress_button.grid(column=1, row=2, sticky='ew')

def magic(files, home_dir, text_box, quality_combobox):
    if len(files) != 0:
        try:
            quality = quality_combobox.get().split()[0]
            args = [
                '-q',
                '-dNOPAUSE', '-dBATCH', '-dSAFER',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.3',
                f'-dPDFSETTINGS=/{quality}',
                f'-sOutputFile={home_dir}{os.sep}compressed.pdf',
                f'{files[0]}'
            ]
            encoding = locale.getpreferredencoding()
            args = [arg.encode(encoding) for arg in args]
            gs.Ghostscript(*args)
            text_box.delete('1.0', 'end')
            text_box.insert('1.0', 'PDF files has been compressed successfully!\n')
            text_box.insert('end', 'The files are saved in:\n')
            text_box.insert('end', f'{home_dir}{os.sep}compressed.pdf\n')
            files.clear()
        except:
            text_box.insert('end', 'Error occurred!')
    else:
        text_box.delete('1.0', 'end')
        text_box.insert('end', 'No file to compress. Please select one.')
