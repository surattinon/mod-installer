import os
import shutil
import requests
from zipfile import ZipFile
import tkinter as tk
import sys
import subprocess
from threading import Thread


# Define the paths
mods_dir = os.path.expandvars("%APPDATA%/.minecraft/mods")
#mods_zip_path = os.path.join(os.path.expandvars("%TEMP%"), "mods.zip")
forge_url = "http://www.basgetbored.me/modpacks/forge.jar"
mods_folder_url = "http://www.basgetbored.me/modpacks/mods"

# Define the GUI functions
# Define the GUI functions
def install_mods_only():
    # Disable the buttons
    mods_only_button.config(state=tk.DISABLED)
    forge_mods_button.config(state=tk.DISABLED)

    # Redirect the standard output to the text widget
    sys.stdout = output_text_widget

    # Run the code in a separate thread
    thread = Thread(target=install_mods_only_thread)
    thread.start()

def install_mods_only_thread():
    try:
        # Delete existing mods
        delete_existing_mods()

        # Download and extract mods folder
        download_mods_folder()

        # Clean up temporary files
        cleanup_temp_files()


        # Print completion message
        output_text_widget.insert(tk.END, "Mod packs installed!!\nPress PLAY Button to start MINECRAFT and Enjoy Krubb ~~~ ^ ^\n", "bold")
        output_text_widget.insert(tk.END, "or press EXIT Button to exit\n")
        output_text_widget.see(tk.END)  # Scroll to the end of the text widget

    except Exception as e:
        output_text_widget.insert(tk.END, "Error: {}\n".format(e))


def install_forge_and_mods():
    # Disable the buttons
    mods_only_button.config(state=tk.DISABLED)
    forge_mods_button.config(state=tk.DISABLED)

    # Redirect the standard output to the text widget
    sys.stdout = output_text_widget

    # Run the code in a separate thread
    thread = Thread(target=install_forge_and_mods_thread)
    thread.start()

def install_forge_and_mods_thread():
    try:
        # Download and install Forge if necessary
        install_forge()

        # Delete existing mods
        delete_existing_mods()

        # Download and extract mods folder
        download_mods_folder()

        # Clean up temporary files
        cleanup_temp_files()


        # Print completion message
        output_text_widget.insert(tk.END, "Mod packs installed!!\nPress PLAY Button to start MINECRAFT and Enjoy Krubb ~~~ ^ ^\n", "bold")
        output_text_widget.insert(tk.END, "or press EXIT Button to exit\n")
        output_text_widget.see(tk.END)  # Scroll to the end of the text widget

    except Exception as e:
        output_text_widget.insert(tk.END, "Error: {}\n".format(e))

def install_forge():
    jar_filename = os.path.basename(forge_url)
    jar_name = os.path.splitext(jar_filename)[0]
    jar_path = os.path.join(os.path.expanduser("~"), jar_filename)

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
        process = subprocess.Popen(["java", "-jar", jar_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True)
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

import requests
import os
import shutil

import requests
import os
import shutil

def download_mods_folder():
    # Print message before downloading mods folder
    output_text_widget.insert(tk.END, "Downloading mod packs for Neko cafe' server\n")
    output_text_widget.see(tk.END)  # Scroll to the end of the text widget

    # Download mods folder
    response = requests.get(mods_folder_url)

    if response.status_code == 200:
        try:
            file_list = response.json()  # Assuming the server returns a JSON list of files
            for file_name in file_list:
                file_url = mods_folder_url + file_name
                file_path = os.path.join(mods_dir, file_name)

                # Download individual file
                response = requests.get(file_url, stream=True)
                with open(file_path, "wb") as file:
                    shutil.copyfileobj(response.raw, file)
                del response

            # Print message after downloading mods folder
            output_text_widget.insert(tk.END, "Mod packs downloaded successfully!\n")
        except ValueError:
            output_text_widget.insert(tk.END, "Invalid response from server. Failed to download mod packs.\n")
    else:
        output_text_widget.insert(tk.END, "Failed to connect to the server. Mod packs download failed.\n")

    output_text_widget.see(tk.END)  # Scroll to the end of the text widget


def zip_mods_folder():
    # Zip mods folder
    output_text_widget.insert(tk.END, "Zipping mods folder\n")
    output_text_widget.see(tk.END)  # Scroll to the end of the text widget
    with ZipFile(mods_zip_path, "w") as zip_file:
        zip_file.write(mods_dir, arcname="mods")

def extract_mods():
    # Extract mods.zip to %appdata%/.minecraft
    output_text_widget.insert(tk.END, "Extracting mod packs\n")
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
    # Open Minecraft launcher
    #os.system('start Minecraft.exe')  # Replace "path_to_minecraft_launcher.exe" with the actual path to the Minecraft launcher executable
    #app_name = "Minecraft.exe"
    #os.system(f"start {app_name}")
    subprocess.run('shell:AppsFolder\\Microsoft.4297127D64EC6_8wekyb3d8bbwe!Minecraft')

    # Exit the application
    exit_program()

# Create the GUI window
window = tk.Tk()
window.title("Neko Cafe' Server Launcher")
window.geometry("720x500")  # Set window size
window.resizable(False, False)  # Lock window size

# Create a title label
title_label = tk.Label(window, text="Neko Cafe' Server Launcher", font=("Arial", 16, "bold"), anchor="w")
title_label.pack(pady=10, padx=10, anchor="w")

# Create a description label
desc_label = tk.Label(window, text="Click the button to install mod packs for Neko cafe' server.",
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

# Run the bold function to configure the "bold" font
bold()

# Run the GUI event loop
window.mainloop()