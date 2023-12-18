import os
import shutil
import requests
from zipfile import ZipFile
import tkinter as tk
import sys
import subprocess
from threading import Thread
from PIL import Image, ImageTk
import base64
import json
import urllib.request
from pathlib import Path
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
import winsound
from tkinter import messagebox

# Define the paths
mods_dir = os.path.expandvars("%APPDATA%/.minecraft/mods")
mods_zip_path = os.path.join(os.path.expandvars("%TEMP%"), "mods.zip")
forge_url = "http://fileserver.basgetbored.me/forge.jar"
mods_url = "http://fileserver.basgetbored.me/mods.zip"

# Specify the path to the Minecraft launcher profiles JSON file
profiles_file_path = os.path.expandvars('%APPDATA%/.minecraft/launcher_profiles.json')

# Specify the profile name for which you want to change the image
new_profile_name = 'Neko Cafe'

# Specify the current profile name
current_profile_name = 'forge'

# Specify the URL of the image
image_url = 'http://fileserver.basgetbored.me/logo/nekoCafeLogo.png'

# Specify the path to save the downloaded image
image_directory = os.path.expandvars('%APPDATA%/.minecraft/libraries/profileLogo')
os.makedirs(image_directory, exist_ok=True)
image_file_path = os.path.join(image_directory, 'nekoCafeLogo.png')

# Download the image from the URL and save it locally
urllib.request.urlretrieve(image_url, image_file_path)


# Define the GUI functions
def install_mods_only():
    # Prompt a warning message
    confirmation = messagebox.askokcancel("WARNING!!", "ทุก Mod ที่คุณเคยติดตั้งทั้งหมดจะถูกลบ และแทนที่ด้วย Modpacks ใหม่\nคุณต้องการที่จะติดตั้งหรือไม่?",
                                          icon='warning')
    if not confirmation:
        return
    # Disable the buttons
    mods_only_button.config(state=tk.DISABLED)
    forge_mods_button.config(state=tk.DISABLED)
    play_button.config(state=tk.DISABLED)
    play_button.config(bg='gray')

    # Redirect the standard output to the text widget
    sys.stdout = output_text_widget

    # Run the code in a separate thread
    thread = Thread(target=install_mods_only_thread)
    thread.start()

def install_mods_only_thread():
    try:
        # Delete existing mods
        delete_existing_mods()

        # Download and extract mods.zip
        download_mods()
        extract_mods()

        # Clean up temporary files
        cleanup_temp_files()

        # Print completion message
        #output_text_widget.insert(tk.END, "Mod packs installed!!\nPress \"PLAY\" Button to start game and Enjoy Krubb ~~~ ^ ^\n", "bold")
        #output_text_widget.insert(tk.END, "or press \"EXIT\" Button to exit and Enjoy Krubb ~~~ ^ ^\n")
        output_text_widget.insert(tk.END, "Mod packs installed!!\npress \"EXIT\" Button to exit and Enjoy Krubb ~~~ ^ ^\n", "bold")
        output_text_widget.see(tk.END)  # Scroll to the end of the text widget
        play_button.config(state=tk.NORMAL)
        play_button.config(bg='green')

    except Exception as e:
        output_text_widget.insert(tk.END, "Error: {}\n".format(e))

def install_forge_and_mods():
    if not messagebox.askokcancel("WARNING!!", "ม้อดทุกม้อดที่คุณเคยลงทั้งหมดจะถูกลบ และแทนที่ด้วย Modpacks ใหม่"):
        return
    # Disable the buttons
    mods_only_button.config(state=tk.DISABLED)
    forge_mods_button.config(state=tk.DISABLED)
    play_button.config(state=tk.DISABLED)
    play_button.config(bg='gray')

    # Redirect the standard output to the text widget
    sys.stdout = output_text_widget

    # Run the code in a separate thread
    thread = Thread(target=install_forge_and_mods_thread)
    thread.start()

def install_forge_and_mods_thread():
    try:
        # Download and install Forge if necessary
        install_forge()
        change_profile()

        # Delete existing mods
        delete_existing_mods()

        # Download and extract mods.zip
        download_mods()
        extract_mods()

        # Clean up temporary files
        cleanup_temp_files()

        # Print completion message
        #output_text_widget.insert(tk.END, "Mod packs installed!!\nPress \"PLAY\" Button to start game and Enjoy Krubb ~~~ ^ ^\n", "bold")
        #output_text_widget.insert(tk.END, "or press \"EXIT\" Button to exit and Enjoy Krubb ~~~ ^ ^\n")
        output_text_widget.insert(tk.END, "Mod packs installed!!\npress \"EXIT\" Button to exit and Enjoy Krubb ~~~ ^ ^\n", "bold")
        output_text_widget.see(tk.END)  # Scroll to the end of the text widget
        play_button.config(state=tk.NORMAL)
        play_button.config(bg='green')

    except Exception as e:
        output_text_widget.insert(tk.END, "Error: {}\n".format(e))

def install_forge():
    jar_filename = os.path.basename(forge_url)
    jar_name = os.path.splitext(jar_filename)[0]
    jar_path = os.path.join(os.path.expanduser("~"), jar_filename)
    forgeCLI = resource_path3("ForgeCLI.jar")
    appdata_path = Path.home() / 'AppData' / 'Roaming'
    forge_target = appdata_path / '.minecraft'

    version_folder_name = jar_name
    versions_dir = os.path.expandvars("%APPDATA%/.minecraft/versions")
    version_folder_path = os.path.join(versions_dir, version_folder_name)

    # Check if Forge version is different
    if not os.path.exists(version_folder_path):
        response = requests.get(forge_url, stream=True)
        with open(jar_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        del response

        # Install jar file
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            ["java", "-jar", forgeCLI, "--installer", jar_path, "--target", forge_target, "--nogui"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=startupinfo
        )
        for line in iter(process.stdout.readline, ''):
            output_text_widget.insert(tk.END, line.rstrip('\n') + '\n')
            output_text_widget.see(tk.END)  # Scroll to the end of the text widget

    else:
        output_text_widget.insert(tk.END, "Forge version already installed. Skipping JAR download and installation.\n")
        output_text_widget.see(tk.END)  # Scroll to the end of the text widget

def delete_existing_mods():
    if os.path.exists(mods_dir):
        file_list = os.listdir(mods_dir)
        for file_name in file_list:
            file_path = os.path.join(mods_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

def download_mods():
    # Print message before downloading mods.zip
    output_text_widget.insert(tk.END, "Downloading mod packs for Neko cafe' server ....\n")
    output_text_widget.see(tk.END)  # Scroll to the end of the text widget

    # Download mods.zip file
    response = requests.get(mods_url, stream=True)
    with open(mods_zip_path, "wb") as file:
        shutil.copyfileobj(response.raw, file)
    del response

def extract_mods():
    # Extract mods.zip to %appdata%/.minecraft
    output_text_widget.insert(tk.END, "Extracting mod packs ....\n")
    output_text_widget.see(tk.END)  # Scroll to the end of the text widget
    with ZipFile(mods_zip_path, "r") as zip_ref:
        file_list = zip_ref.namelist()
        total_files = len(file_list)
        extracted_files = 0
        for file in file_list:
            zip_ref.extract(file, mods_dir)
            extracted_files += 1

def cleanup_temp_files():
    # Clean up temporary files
    os.remove(mods_zip_path)

def exit_program():
    window.destroy()

def bold():
    output_text_widget.tag_configure("bold", font=("Courier New", 14, "bold"))

def play_game():
    # Create a top-level dialog window
    dialog = tk.Toplevel(window)
    dialog.title("Choose Launcher")

    #dialog.geometry("400x170")  # Set window size
    dialog.resizable(False, False)  # Lock window size
    
     # Create a label and checkbox for each launcher option
    launcher_options = [("Minecraft Launcher", "launcher1"),
                        ("TLauncher", "launcher2"),
                        ("Custom Launcher", "custom")]
    
    selected_launcher = tk.StringVar(value="launcher1")  # Set the default selection to "launcher1"
    custom_path_entry = None
    
    def toggle_custom_path_entry():
        if selected_launcher.get() == "custom":
            custom_path_entry.config(state="normal")
            browse_button.config(state="normal")
        else:
            custom_path_entry.config(state="disabled")
            browse_button.config(state="disabled")

    def browse_launcher_path(entry_field):
        if selected_launcher.get() == "custom":
            # Open file dialog to select the custom launcher path
            file_path = filedialog.askopenfilename(title="Select Minecraft Launcher", filetypes=(("Executable Files", "*.exe"),))
            if file_path:
                entry_field.delete(0, tk.END)
                entry_field.insert(0, file_path)
    
    for option, value in launcher_options:
        checkbox = ttk.Checkbutton(dialog, text=option, variable=selected_launcher, onvalue=value, command=toggle_custom_path_entry)
        checkbox.pack(anchor="w", padx=10, pady=5)
        
        if value == "custom":
            # Create an entry field for the custom launcher path
            custom_path_entry = ttk.Entry(dialog, state="disabled", width=80)
            custom_path_entry.pack(anchor="w", padx=10, pady=5)
            
            # Create a browse button to select the custom launcher path
            browse_button = ttk.Button(dialog, text="Browse", command=lambda: browse_launcher_path(custom_path_entry))
            browse_button.pack(anchor="w", padx=10, pady=5)
    
    # Load saved custom path from program data
    saved_path = load_saved_path()
    if custom_path_entry:
        custom_path_entry.insert(0, saved_path)
    
    # Create a button to confirm the launcher selection
    confirm_button = ttk.Button(dialog, text="Play", command=lambda: launch_selected_launcher(selected_launcher.get(), custom_path_entry.get() if custom_path_entry else "", dialog))
    confirm_button.pack(pady=10)

    browse_button = ttk.Button(dialog, text="Browse", command=lambda entry_field=custom_path_entry: browse_launcher_path(entry_field))

    
    
    # Center the dialog window on the screen
    dialog.update_idletasks()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (dialog_width // 2)
    y = (screen_height // 2) - (dialog_height // 2)
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    dialog.transient(window)
    dialog.grab_set()
    window.wait_window(dialog)

def browse_launcher_path(entry_field):
    # Open file dialog to select the custom launcher path
    file_path = filedialog.askopenfilename(title="Select Minecraft Launcher", filetypes=(("Executable Files", "*.exe"),))
    if file_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)

    

def load_saved_path():
    # Load the saved custom path from program data
    try:
        with open("launcher_data.json", "r") as file:
            data = json.load(file)
            return data.get("custom_path", "")
    except FileNotFoundError:
        return ""

def save_custom_path(custom_path):
    # Save the custom path in program data
    data = {"custom_path": custom_path}
    with open("launcher_data.json", "w") as file:
        json.dump(data, file)

def launch_selected_launcher(choice, custom_path, dialog):
    if choice == "launcher1":
        # Open Minecraft Launcher 1
        subprocess.run('explorer.exe shell:AppsFolder\\Microsoft.4297127D64EC6_8wekyb3d8bbwe!Minecraft')
    elif choice == "launcher2":
        # Open Minecraft Launcher 2
        subprocess.run('%APPDATA%/.minecraft/TLauncher.exe')
    elif choice == "custom":
        if custom_path:
            # Save the custom path in program data
            save_custom_path(custom_path)

            # Check if the custom launcher program exists
            if os.path.exists(custom_path):
                # Close the custom launcher program if it is running
                os.system(f"taskkill /F /IM {os.path.basename(custom_path)} > nul")

                # Open the custom Minecraft launcher
                subprocess.run(custom_path)
            else:
                # Play a warning sound and show a message box if the custom launcher program is not found
                winsound.MessageBeep(winsound.MB_ICONWARNING)
                messagebox.showwarning("Launcher Not Found", "The specified launcher program was not found.")

    # Close the dialog window
    dialog.destroy()

    # Exit the application
    exit_program()

def resource_path1(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def resource_path2(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def resource_path3(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def change_profile():

    output_text_widget.insert(tk.END, "Creating Neko Cafe Profile .... \n")

    with open(profiles_file_path, 'r') as file:
        profiles_data = json.load(file)
    
    if current_profile_name in profiles_data['profiles']:
        # Get the profile information
        profile = profiles_data['profiles'][current_profile_name]

        # Change the profile name
        profile['name'] = new_profile_name

        # Remove the old profile entry
        profiles_data['profiles'].pop(current_profile_name)

        # Add the modified profile entry with the new name
        profiles_data['profiles'][new_profile_name] = profile

        # Save the modified profiles data back to the JSON file
        with open(profiles_file_path, 'w') as file:
            json.dump(profiles_data, file, indent=4)
    else:
        print(f"Profile '{current_profile_name}' not found.")

        # Check if the specified profile exists
    if new_profile_name in profiles_data['profiles']:
        # Read the image data from the local file
        with open(image_file_path, 'rb') as img:
            image_data = img.read()

        # Convert the image data to base64 format
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Get the profile information
        profile = profiles_data['profiles'][new_profile_name]

        jvm_argument = "-Xmx4G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"

        profile['javaArgs'] = jvm_argument

        img_format = "data:image/png;base64,"

        # Add or update the profile image information
        if 'icon' in profile:
            profile['icon'] = img_format + base64_image

        # Save the modified profiles data back to the JSON file
        with open(profiles_file_path, 'w') as img:
            json.dump(profiles_data, img, indent=4)
    else:
        print(f"Profile '{new_profile_name}' not found.")

def show_custom_warning_message(title, message):
    dialog = tk.Toplevel(window)
    dialog.title(title)

    label = tk.Label(dialog, text=message, font=("Arial", 14), padx=20, pady=20)
    label.pack()

    ok_button = tk.Button(dialog, text="OK", command=lambda: dialog.destroy(), font=("Arial", 12))
    ok_button.pack(pady=10)

    dialog.transient(window)
    dialog.grab_set()
    window.wait_window(dialog)

    return messagebox.askokcancel(title, message)

# Create the GUI window
window = tk.Tk()
window.title("Neko Cafe' Server Launcher")
window.geometry("720x500")  # Set window size
window.resizable(False, False)  # Lock window size

icon_path = (resource_path1("Neko-Cafe_-Launcher-logo.ico"))  # Replace "path_to_your_icon_file.ico" with the actual path to your icon file
window.iconbitmap(icon_path)

# Load the logo image
logo_path = (resource_path2("Neko Cafe'.png"))  # Replace with the actual path to your logo image
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((50, 50))  # Resize the logo image as per your requirement
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a label for the logo
logo_label = tk.Label(window, image=logo_photo)
logo_label.pack(pady=10, padx=10, anchor="nw")

# Create a title label
title_label = tk.Label(window, text="Neko Cafe' Launcher", font=("Arial", 16, "bold"), anchor="w")
title_label.pack(pady=10, padx=10, anchor="w")

# Create a description label
desc_label = tk.Label(window, text="Click the install button to install mod packs for Neko cafe' server.",
                      anchor="w")
desc_label.pack(pady=10, padx=10, anchor="w")

# Create a frame to hold buttons
button_frame = tk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=10, padx=10, anchor="e")

# Create the PLAY button
play_button = tk.Button(button_frame, text="PLAY", command=play_game, font=("Arial", 14, "bold"), bg="green", fg="white", width=15, height=2)
play_button.pack(side=tk.LEFT, padx=(0,40))

# Create the "Install Only Mods" button
mods_only_button = tk.Button(button_frame, text="Install Only Mods", command=install_mods_only, width=20, height=2)
mods_only_button.pack(side=tk.RIGHT, padx=5)

# Create the "Install Forge and Mods" button
forge_mods_button = tk.Button(button_frame, text="Install Forge and Mods", command=install_forge_and_mods, width=20, height=2)
forge_mods_button.pack(side=tk.RIGHT, padx=5)

# Create the exit button
exit_button = tk.Button(button_frame, text="Exit", command=exit_program, width=15, height=2)
exit_button.pack(side=tk.RIGHT, padx=5)


# Create a text widget to show the running status
output_text_widget = tk.Text(window, height=20, width=80, font=("Courier New", 10), wrap=tk.WORD)
output_text_widget.tag_configure("bold", font=("Courier New", 14, "bold"))  # Configure "bold" font
output_text_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create a scroll bar for the text widget
scrollbar = tk.Scrollbar(output_text_widget)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=output_text_widget.yview)
output_text_widget.config(yscrollcommand=scrollbar.set)

# Center the window on the screen
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Run the bold function to configure the "bold" font
bold()

# Run the GUI event loop
window.mainloop()