import tkinter as tk
from PIL import Image, ImageTk
import merge
import split
import rotate
import compress

root = tk.Tk()
root.title('Easy PDF v0.1')
root.resizable(0,0)

# window
canvas = tk.Canvas(root)
canvas.grid(columnspan=2, rowspan=3)

# logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(columnspan=2, row=0)

# merge button
merge_button = tk.Button(root, text="Merge", command=lambda:merge.merge(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg="#ff474a", fg="white", font="Raleway", height=3)
merge_button.grid(column=0, row=1, sticky="ew")

# split button
split_button = tk.Button(root, text="Split", command=lambda:split.split(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg="#ff474a", fg="white", font="Raleway", height=3)
split_button.grid(column=1, row=1, sticky="ew")

# rotate button
rotate_button = tk.Button(root, text="Rotate", command=lambda:rotate.rotate(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg="#ff474a", fg="white", font="Raleway", height=3)
rotate_button.grid(column=0, row=2, sticky="ew")

# compress button
compress_button = tk.Button(root, text="Compress", command=lambda:compress.compress(logo_label, merge_button, split_button, rotate_button, compress_button, root), bg="#ff474a", fg="white", font="Raleway", height=3)
compress_button.grid(column=1, row=2, sticky="ew")

root.mainloop()
