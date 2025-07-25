import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Functions for button actions
def project_info():
    messagebox.showinfo("Project Info", "This project helps prevent unauthorized webcam access.")

def view_logs():
    messagebox.showinfo("Logs", "No suspicious activity detected.")

def check_status():
    messagebox.showinfo("Status", "Webcam is currently disabled.")

def change_password():
    messagebox.showinfo("Change Password", "Password change feature not implemented.")

def disable_camera():
    messagebox.showinfo("Camera", "Webcam has been disabled.")

def enable_camera():
    messagebox.showinfo("Camera", "Webcam has been enabled.")

# GUI Setup
root = tk.Tk()
root.title("Web Cam Security")
root.geometry("500x650")
root.configure(bg="black")

# Define style for rounded buttons using ttk
style = ttk.Style()
style.configure("Rounded.TButton",
                foreground="black",
                background="white",
                font=("Arial", 10, "bold"),
                padding=6,
                borderwidth=2)
style.map("Rounded.TButton",
          background=[("active", "#cc0000")])

# Title Button - Project Info
ttk.Button(root, text="Project Info", style="Rounded.TButton", command=project_info).pack(pady=10)

# Main Heading
tk.Label(root, text="WebCam Spyware Security", bg="black", fg="white", font=("Arial", 16, "bold")).pack(pady=10)

# Load webcam-block icon image
try:
    image = Image.open("image.png")  # Ensure this image is in the same directory
    image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    tk.Label(root, image=photo, bg="black").pack()
except:
    tk.Label(root, text="[WebCam Block Icon Here]", bg="black", fg="white").pack(pady=50)

# Row of Buttons: View Logs and Check Status
frame1 = tk.Frame(root, bg="black")
frame1.pack(pady=10)

ttk.Button(frame1, text="View Logs", style="Rounded.TButton", command=view_logs).pack(side="left", padx=10)
ttk.Button(frame1, text="Check Status", style="Rounded.TButton", command=check_status).pack(side="left", padx=10)

# Change Password Button
ttk.Button(root, text="Change Password", style="Rounded.TButton", command=change_password).pack(pady=10)

# Bottom Panel for Enable/Disable Camera
frame2 = tk.Frame(root, bg="gray", padx=20, pady=20)
frame2.pack(pady=20)

ttk.Button(frame2, text="Disable Camera", style="Rounded.TButton", command=disable_camera).pack(pady=10)
ttk.Button(frame2, text="Enable Camera", style="Rounded.TButton", command=enable_camera).pack(pady=10)

root.mainloop()
