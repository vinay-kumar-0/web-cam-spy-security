import os
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import hashlib
import winreg
root = tk.Tk()
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
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
        webcam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        value, _ = winreg.QueryValueEx(webcam_key, "Value")
        winreg.CloseKey(webcam_key)

        if value == "Deny":
            status = "Disabled"
        elif value == "Allow":
            status = "Enabled"
        else:
            status = "Unknown"

        messagebox.showinfo("Status", f"Webcam status: {status}")
    except FileNotFoundError:
        messagebox.showinfo("Status", "Webcam status: Unknown (registry key not found)")
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
            try:
                webcam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                webcam_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)

            winreg.SetValueEx(webcam_key, "Value", 0, winreg.REG_SZ, "Deny")
            winreg.CloseKey(webcam_key)

            # Confirm the change
            webcam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            value, _ = winreg.QueryValueEx(webcam_key, "Value")
            winreg.CloseKey(webcam_key)

            if value == "Deny":
                log_action("Webcam access DENIED via registry")
                messagebox.showinfo("Camera Access", "Webcam access has been denied.")
            else:
                messagebox.showwarning("Camera Access", "Failed to confirm registry change.")

        except PermissionError:
            messagebox.showerror("Permission Error", "Run this script as Administrator to modify registry.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update registry.\n{e}")

def enable_camera():
    if prompt_password():
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
            try:
                webcam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                webcam_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)

            winreg.SetValueEx(webcam_key, "Value", 0, winreg.REG_SZ, "Allow")
            winreg.CloseKey(webcam_key)

            # Confirm the change
            webcam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            value, _ = winreg.QueryValueEx(webcam_key, "Value")
            winreg.CloseKey(webcam_key)

            if value == "Allow":
                log_action("Webcam access ALLOWED via registry")
                messagebox.showinfo("Camera Access", "Webcam access has been allowed.")
            else:
                messagebox.showwarning("Camera Access", "Failed to confirm registry change.")

        except PermissionError:
            messagebox.showerror("Permission Error", "Run this script as Administrator to modify registry.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update registry.\n{e}")
class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, command, **kwargs):
        super().__init__(parent, width=60, height=30, bg=parent['bg'], highlightthickness=0, **kwargs)
        self.command = command
        self.theme = "light"

        # Background oval
        self.bg_rect = self.create_oval(5, 5, 55, 25, fill="#ccc", outline="#ccc")
        # Movable circle
        self.indicator = self.create_oval(30, 5, 50, 25, fill="#00BFFF", outline="")

        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        if self.theme == "light":
            self.theme = "dark"
            self.itemconfig(self.indicator, fill="#444")
            self.coords(self.indicator, 10, 5, 30, 25)
        else:
            self.theme = "light"
            self.itemconfig(self.indicator, fill="#00BFFF")
            self.coords(self.indicator, 30, 5, 50, 25)
        
        self.command(self.theme)



themes = {
    "light": {
        "bg": "#F6F5F5",
        "fg": "black",
        "btn_bg": "white",
        "btn_fg": "black"
    },
    "dark": {
        "bg": "#2E2E2E",
        "fg": "#F6F5F5",
        "btn_bg": "#4E4E4E",
        "btn_fg": "black"
    }
}

def apply_theme(theme_name):
    theme = themes[theme_name]
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Frame):
            widget.configure(bg=theme["bg"])
        elif isinstance(widget, ttk.Button):
            style.configure("Rounded.TButton",
                            foreground=theme["btn_fg"],
                            background=theme["btn_bg"])

def on_theme_change(new_theme):
    apply_theme(new_theme)

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, command, **kwargs):
        super().__init__(parent, width=60, height=30, bg=parent['bg'], highlightthickness=0, **kwargs)
        self.command = command
        self.theme = "light"
        self.bg_rect = self.create_oval(5, 5, 55, 25, fill="#ccc", outline="#ccc")
        self.indicator = self.create_oval(30, 5, 50, 25, fill="#00BFFF", outline="")
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        if self.theme == "light":
            self.theme = "dark"
            self.itemconfig(self.indicator, fill="#444")
            self.coords(self.indicator, 10, 5, 30, 25)
        else:
            self.theme = "light"
            self.itemconfig(self.indicator, fill="#00BFFF")
            self.coords(self.indicator, 30, 5, 50, 25)
        self.command(self.theme)


def get_webcam_status():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
        webcam_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        value, _ = winreg.QueryValueEx(webcam_key, "Value")
        winreg.CloseKey(webcam_key)

        if value == "Deny":
            return "Disabled"
        elif value == "Allow":
            return "Enabled"
        else:
            return "Unknown"
    except FileNotFoundError:
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"


def update_status_label():
    status = get_webcam_status()
    status_label.config(text=f"Webcam Status: {status}", fg="green" if status == "Enabled" else "red")
    root.after(5000, update_status_label)  # Refresh every 5 seconds




# GUI Setup

root.title("Web Cam Security")
root.geometry("500x650")
root.configure(bg="#F6F5F5")

#status indidcator
status_label = tk.Label(root, text="Webcam Status: Checking...", bg="#F6F5F5", fg="black", font=("Arial", 10, "bold"))
status_label.place(x=10, y=15)  # Adjust position as needed

#theme toggle switch
toggle = ToggleSwitch(root, command=on_theme_change)
toggle.place(x=440, y=10)  # adjust coordinates based on your layout


# themes


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


#theme toggle button


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
update_status_label()
root.mainloop()
