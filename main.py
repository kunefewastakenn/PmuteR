import tkinter as tk
from tkinter import ttk, messagebox
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from collections import defaultdict
from plyer import notification
import keyboard

keybindings = {}

def toggle_mute(application_name):
    sessions = AudioUtilities.GetAllSessions()
    found = False 
    for session in sessions:
        if session.Process and session.Process.name().lower() == application_name.lower():
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            current_mute_status = volume.GetMute()
            volume.SetMute(not current_mute_status, None)
            notification.notify(title=f"PyMuteR", message=f"{'Muted' if not current_mute_status else 'Unmuted'} {application_name}", timeout=0.2)
            found = True
    if not found:
        print(f"Application '{application_name}' not found!")


def add_keybinding():
    app_name = program_var.get()
    key = keybind_var.get()

    if not app_name or not key:
        messagebox.showwarning("Input correctly mate!", "Dare you to select a program and enter a keybind")
        return

    if key in keybindings:
        messagebox.showwarning("Keybind confliction", f"keybind '{key}' is already assigned to another application plise change it")
        return

    keybindings[key] = app_name
    keyboard.add_hotkey(key, lambda: toggle_mute(app_name))

    keybinding_list.insert(tk.END, f"{key} -> {app_name}")
    keybind_var.set("")


from collections import defaultdict

def print_audio_sessions():
    sessions = AudioUtilities.GetAllSessions()
    seen_apps = set()

    print("Active audio sessions (unique):")
    for session in sessions:
        if session.Process and session.Process.name() not in seen_apps:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            mute_status = "muted" if volume.GetMute() else "unmuted"
            print(f" - {session.Process.name()} ({mute_status})")
            seen_apps.add(session.Process.name())
        elif not session.Process and "System sounds" not in seen_apps:
            print(" - System sounds (unmuted)")
            seen_apps.add("System sounds")




def refresh_programs():
    programs = get_audio_sessions()
    program_dropdown["values"] = programs
    if programs:
        program_var.set(programs[0])

def remove_keybinding():
    key = keybind_var.get()
    if key in keybindings:
        del keybindings[key]
        keyboard.remove_hotkey(key)
        keybinding_list.delete(0, tk.END)
        for key, app in keybindings.items():
            keybinding_list.insert(tk.END, f"{key} -> {app}")
        keybind_var.set("")


def get_audio_sessions():
    sessions = AudioUtilities.GetAllSessions()
    processes = []
    for session in sessions:
        if session.Process:
            processes.append(session.Process.name())
    return list(set(processes))


root = tk.Tk()
root.title("PyMuteR")
root.geometry("500x400")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

program_var = tk.StringVar()
ttk.Label(frame, text="Select Program:").grid(row=0, column=0, sticky=tk.W)
program_dropdown = ttk.Combobox(frame, textvariable=program_var, state="readonly", width=40)
program_dropdown.grid(row=0, column=1, sticky=tk.W)

# refresh button
refresh_button = ttk.Button(frame, text="Refresh", command=refresh_programs)
refresh_button.grid(row=0, column=2, sticky=tk.E)

#printing audio sessions
refresh_button = ttk.Button(frame, text="Print audio sessions", command=print_audio_sessions)
refresh_button.grid(row=10, column=2, sticky=tk.E)

#remov keyindd
refresh_button = ttk.Button(frame, text="Remove Keybind", command=remove_keybinding)
refresh_button.grid(row=2, column=2, sticky=tk.E)

# keybind inputd
keybind_var = tk.StringVar()
ttk.Label(frame, text="Enter Keybind:").grid(row=1, column=0, sticky=tk.W)
keybind_entry = ttk.Entry(frame, textvariable=keybind_var, width=30)
keybind_entry.grid(row=1, column=1, sticky=tk.W)

add_button = ttk.Button(frame, text="Add Keybind", command=add_keybinding)
add_button.grid(row=1, column=2, sticky=tk.E)

# Keybindi list
ttk.Label(frame, text="Assigned Keybinds:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
keybinding_list = tk.Listbox(frame, height=10, width=60)
keybinding_list.grid(row=4, column=0, columnspan=3, pady=(0, 10))

footer_label = tk.Label(root, text="made by @kunefewastakenn", font=("Arial", 9), anchor="se")
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

footer_label = tk.Label(root, text="write your keybind with using ""+"" example (ctrl+k)", font=("Arial", 9), anchor="se")
footer_label.place(relx=1.0, rely=1.0, anchor="se", x=-235, y=-10)


refresh_programs()
root.mainloop()