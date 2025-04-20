import os
import sys
import winreg as reg
import tkinter as tk
from tkinter import filedialog, messagebox

def add_to_startup(file_path, app_name):
    """Add the application to Windows startup registry"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        
        # Set the value
        reg.SetValueEx(key, app_name, 0, reg.REG_SZ, file_path)
        
        # Close the key
        reg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error adding to startup: {e}")
        return False

def remove_from_startup(app_name):
    """Remove the application from Windows startup registry"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        
        # Delete the value
        reg.DeleteValue(key, app_name)
        
        # Close the key
        reg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error removing from startup: {e}")
        return False

def check_if_in_startup(app_name):
    """Check if the application is already in startup registry"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_READ)
        
        # Try to get the value
        reg.QueryValueEx(key, app_name)
        
        # Close the key
        reg.CloseKey(key)
        return True
    except:
        return False

def create_gui():
    """Create a simple GUI for the startup manager"""
    root = tk.Tk()
    root.title("Startup Manager")
    root.geometry("400x300")
    root.resizable(False, False)
    
    # Application variables
    app_path = tk.StringVar()
    app_name = tk.StringVar()
    
    # Functions
    def browse_file():
        filename = filedialog.askopenfilename(
            title="Select Application",
            filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        if filename:
            app_path.set(filename)
            # Set default app name from file name
            default_name = os.path.splitext(os.path.basename(filename))[0]
            app_name.set(default_name)
    
    def add_app():
        path = app_path.get()
        name = app_name.get()
        
        if not path or not name:
            messagebox.showerror("Error", "Please select an application and provide a name.")
            return
            
        if check_if_in_startup(name):
            if messagebox.askyesno("Already exists", 
                                  f"{name} is already in startup. Do you want to update it?"):
                remove_from_startup(name)
            else:
                return
                
        if add_to_startup(path, name):
            messagebox.showinfo("Success", f"{name} has been added to startup!")
        else:
            messagebox.showerror("Error", "Failed to add to startup.")
    
    def remove_app():
        name = app_name.get()
        
        if not name:
            messagebox.showerror("Error", "Please provide the application name.")
            return
            
        if not check_if_in_startup(name):
            messagebox.showerror("Error", f"{name} is not in startup.")
            return
            
        if remove_from_startup(name):
            messagebox.showinfo("Success", f"{name} has been removed from startup!")
        else:
            messagebox.showerror("Error", "Failed to remove from startup.")
    
    # GUI Layout
    tk.Label(root, text="Add Application to Startup", font=("Arial", 14)).pack(pady=10)
    
    # Application path frame
    path_frame = tk.Frame(root)
    path_frame.pack(fill="x", padx=20, pady=5)
    
    tk.Label(path_frame, text="Application Path:").pack(anchor="w")
    
    path_input_frame = tk.Frame(path_frame)
    path_input_frame.pack(fill="x", pady=5)
    
    tk.Entry(path_input_frame, textvariable=app_path, width=30).pack(side="left", fill="x", expand=True)
    tk.Button(path_input_frame, text="Browse", command=browse_file).pack(side="right", padx=5)
    
    # Application name frame
    name_frame = tk.Frame(root)
    name_frame.pack(fill="x", padx=20, pady=5)
    
    tk.Label(name_frame, text="Application Name:").pack(anchor="w")
    tk.Entry(name_frame, textvariable=app_name, width=30).pack(fill="x", pady=5)
    
    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(fill="x", padx=20, pady=20)
    
    tk.Button(buttons_frame, text="Add to Startup", command=add_app, bg="#4CAF50", fg="white", 
             width=15).pack(side="left", padx=10)
    tk.Button(buttons_frame, text="Remove from Startup", command=remove_app, bg="#F44336", fg="white", 
             width=15).pack(side="right", padx=10)
    
    # Status frame
    status_frame = tk.Frame(root)
    status_frame.pack(fill="x", side="bottom", padx=20, pady=10)
    
    status_label = tk.Label(status_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(fill="x")
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()