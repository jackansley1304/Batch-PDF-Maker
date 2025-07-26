from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, Button, Scrollbar, SINGLE

def images_to_pdf(image_paths, output_pdf):
    images = []
    
    for path in image_paths:
        img = Image.open(path).convert('RGB')
        images.append(img)

    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        messagebox.showinfo("Success", f"PDF saved as {output_pdf}")
    else:
        messagebox.showwarning("Warning", "No images found.")

def choose_folder_and_manage():
    folder = filedialog.askdirectory(title="Select Image Folder")
    if not folder:
        return

    files = [f for f in sorted(os.listdir(folder)) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    image_paths = [os.path.join(folder, f) for f in files]

    if not image_paths:
        messagebox.showwarning("Warning", "No images found in selected folder.")
        return

    manager = tk.Toplevel()
    manager.title("Manage Image Order and Deletion")

    listbox = Listbox(manager, selectmode=SINGLE, width=60)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(manager, command=listbox.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    for img in image_paths:
        listbox.insert(tk.END, os.path.basename(img))

    def move_up():
        index = listbox.curselection()
        if not index or index[0] == 0:
            return
        i = index[0]
        image_paths[i], image_paths[i - 1] = image_paths[i - 1], image_paths[i]
        listbox.delete(0, tk.END)
        for img in image_paths:
            listbox.insert(tk.END, os.path.basename(img))
        listbox.select_set(i - 1)

    def move_down():
        index = listbox.curselection()
        if not index or index[0] == len(image_paths) - 1:
            return
        i = index[0]
        image_paths[i], image_paths[i + 1] = image_paths[i + 1], image_paths[i]
        listbox.delete(0, tk.END)
        for img in image_paths:
            listbox.insert(tk.END, os.path.basename(img))
        listbox.select_set(i + 1)

    def delete_selected():
        index = listbox.curselection()
        if not index:
            return
        i = index[0]
        del image_paths[i]
        listbox.delete(i)

    def generate_pdf():
        default_name = os.path.basename(folder)
        output_pdf = simpledialog.askstring("Output PDF", f"Enter the output PDF file name (without extension):", initialvalue=default_name)
        if not output_pdf:
            messagebox.showerror("Error", "No output filename provided.")
            return
        output_pdf = os.path.join(folder, output_pdf + ".pdf")
        images_to_pdf(image_paths, output_pdf)
        manager.destroy()

    button_frame = tk.Frame(manager)
    button_frame.pack(side=tk.RIGHT, fill=tk.Y)

    Button(button_frame, text="Move Up", command=move_up).pack(padx=5, pady=5)
    Button(button_frame, text="Move Down", command=move_down).pack(padx=5, pady=5)
    Button(button_frame, text="Delete", command=delete_selected).pack(padx=5, pady=5)
    Button(button_frame, text="Generate PDF", command=generate_pdf).pack(padx=5, pady=20)

def main():
    root = tk.Tk()
    root.withdraw()
    choose_folder_and_manage()
    root.mainloop()

if __name__ == "__main__":
    main()
