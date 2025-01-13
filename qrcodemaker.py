import qrcode
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageSequence
import requests

def download_gif(url, path):
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

def generate_qr_code(url, file_path):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image to the specified file path
    img.save(file_path)

def on_generate(event=None):
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        generate_qr_code(url, file_path)
        messagebox.showinfo("Success", f"QR Code saved to {file_path}")

def update_frame(frame_number):
    frame = frames[frame_number]
    frame_number = (frame_number + 1) % len(frames)
    background_label.configure(image=frame)
    root.after(100, update_frame, frame_number)

# Create the main window
root = tk.Tk()
root.title("QR Code Generator")

# Download the GIF
gif_url = "https://media.giphy.com/media/Qgfz2N36MgUBG/giphy.gif"
gif_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'background.gif')
download_gif(gif_url, gif_path)

# Load the GIF
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]

# Create and place the background label
background_label = tk.Label(root)
background_label.pack(fill=tk.BOTH, expand=tk.YES)
update_frame(0)

# Create and place the label
label = tk.Label(root, text="Here you can paste your URL and we will make a QR code for it! 😊", bg="white")
label.pack(pady=10)

# Create and place the entry widget
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.bind("<Return>", on_generate)  # Bind the Enter key to the on_generate function

# Create and place the button
generate_button = tk.Button(root, text="Generate QR Code", command=on_generate)
generate_button.pack(pady=20)

# Set the background color of the window
root.configure(bg="white")

# Run the application
root.mainloop()
