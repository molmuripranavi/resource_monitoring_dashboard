import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Window
root = tk.Tk()
root.title("OS Resource Monitoring Dashboard")
root.geometry("1000x700")
root.configure(bg="black")

# Title
title = tk.Label(
    root,
    text="OS Resource Monitoring Dashboard",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="black"
)
title.pack(pady=10)

# System Info Frame
info_frame = tk.Frame(root, bg="black")
info_frame.pack(pady=5)

cpu_label = tk.Label(info_frame, font=("Arial", 13), fg="green", bg="black")
cpu_label.pack()

mem_label = tk.Label(info_frame, font=("Arial", 13), fg="yellow", bg="black")
mem_label.pack()

disk_label = tk.Label(info_frame, font=("Arial", 13), fg="cyan", bg="black")
disk_label.pack()

net_label = tk.Label(info_frame, font=("Arial", 13), fg="white", bg="black")
net_label.pack()

uptime_label = tk.Label(info_frame, font=("Arial", 13), fg="lightblue", bg="black")
uptime_label.pack()

battery_label = tk.Label(info_frame, font=("Arial", 13), fg="orange", bg="black")
battery_label.pack()

# Process Box
process_title = tk.Label(
    root,
    text="Top Running Processes (CPU %)",
    font=("Arial", 14, "bold"),
    fg="orange",
    bg="black"
)
process_title.pack()

process_box = tk.Text(
    root,
    height=8,
    width=80,
    bg="black",
    fg="orange",
    font=("Courier", 10)
)
process_box.pack(pady=10)

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

cpu_tab = tk.Frame(notebook)
ram_tab = tk.Frame(notebook)
disk_tab = tk.Frame(notebook)
network_tab = tk.Frame(notebook)

notebook.add(cpu_tab, text="CPU Graph")
notebook.add(ram_tab, text="RAM Graph")
notebook.add(disk_tab, text="Disk Graph")
notebook.add(network_tab, text="Network Graph")

# Graphs
fig_cpu, ax_cpu = plt.subplots(figsize=(6,3))
canvas_cpu = FigureCanvasTkAgg(fig_cpu, cpu_tab)
canvas_cpu.get_tk_widget().pack()

fig_ram, ax_ram = plt.subplots(figsize=(6,3))
canvas_ram = FigureCanvasTkAgg(fig_ram, ram_tab)
canvas_ram.get_tk_widget().pack()

fig_disk, ax_disk = plt.subplots(figsize=(6,3))
canvas_disk = FigureCanvasTkAgg(fig_disk, disk_tab)
canvas_disk.get_tk_widget().pack()

fig_net, ax_net = plt.subplots(figsize=(6,3))
canvas_net = FigureCanvasTkAgg(fig_net, network_tab)
canvas_net.get_tk_widget().pack()

cpu_data = []
ram_data = []
disk_data = []
net_data = []

running = True

def update_dashboard():
    global running

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()

    sent = net.bytes_sent // (1024 * 1024)

    # Uptime (Hours + Minutes)
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    # Battery
    battery = psutil.sensors_battery()
    if battery:
        battery_text = f"Battery: {battery.percent}%"
    else:
        battery_text = "Battery: Not Available"

    cpu_label.config(text=f"CPU Usage: {cpu}%")
    mem_label.config(text=f"Memory Usage: {memory}%")
    disk_label.config(text=f"Disk Usage: {disk}%")
    net_label.config(text=f"Network Sent: {sent} MB")
    uptime_label.config(text=f"System Uptime: {hours}h {minutes}m")
    battery_label.config(text=battery_text)

    # Top Processes
    process_box.delete("1.0", tk.END)

    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            processes.append((proc.info['name'], proc.info['cpu_percent']))
        except:
            pass

    processes = sorted(processes, key=lambda x: x[1], reverse=True)

    process_box.insert(tk.END, "Process Name               CPU%\n")
    process_box.insert(tk.END, "-------------------------------------\n")

    for proc in processes[:10]:
        name = proc[0] if proc[0] else "Unknown"
        cpu_percent = proc[1]
        process_box.insert(tk.END, f"{name:<25} {cpu_percent:>5}%\n")

    # Store Data
    cpu_data.append(cpu)
    ram_data.append(memory)
    disk_data.append(disk)
    net_data.append(sent)

    if len(cpu_data) > 20:
        cpu_data.pop(0)
        ram_data.pop(0)
        disk_data.pop(0)
        net_data.pop(0)

    # CPU Graph
    ax_cpu.clear()
    ax_cpu.plot(cpu_data)
    ax_cpu.set_title("CPU Usage")
    canvas_cpu.draw()

    # RAM Graph
    ax_ram.clear()
    ax_ram.plot(ram_data)
    ax_ram.set_title("RAM Usage")
    canvas_ram.draw()

    # Disk Graph
    ax_disk.clear()
    ax_disk.plot(disk_data)
    ax_disk.set_title("Disk Usage")
    canvas_disk.draw()

    # Network Graph
    ax_net.clear()
    ax_net.plot(net_data)
    ax_net.set_title("Network Sent")
    canvas_net.draw()

    if running:
        root.after(1000, update_dashboard)

def on_closing():
    global running
    running = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

update_dashboard()
root.mainloop()