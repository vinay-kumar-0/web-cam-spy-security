import os
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import hashlib

# Functions for button actions
def project_info():
    html_path=os.path.abspath("info.html")
    webbrowser.open(f"file:///{html_path}")

def view_logs():
    log_file = "webcam_logs.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = f.read()
        if logs.strip():
            messagebox.showinfo("Webcam Logs", logs)
        else:
            messagebox.showinfo("Webcam Logs", "No webcam activity detected.")
    else:
        messagebox.showwarning("Logs", "Log file not found.")

def log_action(action):
    with open("webcam_logs.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {action}\n")

def check_status():
    try:
        result = subprocess.check_output(
            'wmic path Win32_PnPEntity where "Name like \'%Camera%\'" get Status',
            shell=True
        ).decode()
        
        # Extract and clean the status
        status_lines = [line.strip() for line in result.splitlines() if line.strip()]
        status = status_lines[-1] if len(status_lines) > 1 else "Unknown"

        messagebox.showinfo("Status", f"Webcam status: {status}")
    except Exception as e:
        messagebox.showerror("Status Error", f"Unable to retrieve webcam status.\n{e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(new_password):
    hashed = hash_password(new_password)
    with open("password.txt", "w") as f:
        f.write(hashed)

def prompt_password():
    def verify():
        entered = password_entry.get()
        with open("password.txt", "r") as f:
            saved_hash = f.read().strip()
        if hash_password(entered) == saved_hash:
            popup.destroy()
            nonlocal is_verified
            is_verified = True
        else:
            messagebox.showerror("Error", "Incorrect Password")
            popup.destroy()

    is_verified = False
    popup = tk.Toplevel()
    popup.title("Enter Password")
    tk.Label(popup, text="Password:").pack(pady=5)
    password_entry = tk.Entry(popup, show="*")
    password_entry.pack(pady=5)
    tk.Button(popup, text="Submit", command=verify).pack(pady=10)
    popup.grab_set()
    popup.wait_window()
    return is_verified


def change_password():
    def update():
        new = new_pass.get()
        confirm = confirm_pass.get()
        if not new or not confirm:
            messagebox.showwarning("Warning", "Fields cannot be empty")
        elif new != confirm:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            save_password(new)
            messagebox.showinfo("Success", "Password changed successfully")
            cp_popup.destroy()

    cp_popup = tk.Toplevel()
    cp_popup.title("Change Password")
    tk.Label(cp_popup, text="New Password:").pack(pady=5)
    new_pass = tk.Entry(cp_popup, show="*")
    new_pass.pack(pady=5)
    tk.Label(cp_popup, text="Confirm Password:").pack(pady=5)
    confirm_pass = tk.Entry(cp_popup, show="*")
    confirm_pass.pack(pady=5)
    tk.Button(cp_popup, text="Update", command=update).pack(pady=10)
    cp_popup.grab_set()

def disable_camera():
    if prompt_password():
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as webcam_key:
                i = 0
                while True:
                    try:
                        app_key_name = winreg.EnumKey(webcam_key, i)
                        with winreg.OpenKey(webcam_key, app_key_name, 0, winreg.KEY_ALL_ACCESS) as app_key:
                            winreg.SetValueEx(app_key, "Value", 0, winreg.REG_SZ, "Deny")
                        i += 1
                    except OSError:
                        break
            log_action("Webcam access DENIED via registry")
            messagebox.showinfo("Camera Access", "Webcam access has been denied for all apps.")
        except PermissionError:
            messagebox.showerror("Permission Error", "Run this script as Administrator to modify registry.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update registry.\n{e}")

def enable_camera():
    if prompt_password():
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as webcam_key:
                i = 0
                while True:
                    try:
                        app_key_name = winreg.EnumKey(webcam_key, i)
                        with winreg.OpenKey(webcam_key, app_key_name, 0, winreg.KEY_ALL_ACCESS) as app_key:
                            winreg.SetValueEx(app_key, "Value", 0, winreg.REG_SZ, "Allow")
                        i += 1
                    except OSError:
                        break
            log_action("Webcam access ALLOWED via registry")
            messagebox.showinfo("Camera Access", "Webcam access has been allowed for all apps.")
        except PermissionError:
            messagebox.showerror("Permission Error", "Run this script as Administrator to modify registry.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update registry.\n{e}")


# GUI Setup
root = tk.Tk()
root.title("Web Cam Security")
root.geometry("500x650")
root.configure(bg="#F6F5F5")

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
tk.Label(root, text="WebCam Spyware Security", bg="white", fg="black", font=("Arial", 16, "bold")).pack(pady=10)

# Load webcam-block icon image
try:
    image = Image.open("image.png")  # Ensure this image is in the same directory
    image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    tk.Label(root, image=photo).pack()
except:
    tk.Label(root, text="[WebCam Block Icon Here]", bg="black", fg="black").pack(pady=50)

# Row of Buttons: View Logs and Check Status
frame1 = tk.Frame(root, bg="#F6F5F5")
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
