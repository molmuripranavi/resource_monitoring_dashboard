# resource_monitoring_dashboard
# OS Resource Monitoring Dashboard

## Overview

The **OS Resource Monitoring Dashboard** is a Python-based desktop application built using **Tkinter**, **Psutil**, and **Matplotlib**. It provides real-time monitoring of system resources such as CPU, Memory, Disk Usage, Network Activity, Battery Status, System Uptime, and Running Processes.

The dashboard also displays graphical representations of resource utilization, making it easier to analyze system performance.

---

## Features

### System Monitoring

* Real-time CPU Usage Monitoring
* Real-time Memory (RAM) Usage Monitoring
* Disk Usage Monitoring
* Network Usage Monitoring
* Battery Status Display
* System Uptime Tracking

### Process Monitoring

* Displays Top 10 Running Processes
* Shows CPU Consumption of Active Processes

### Graphical Visualization

* CPU Usage Graph
* RAM Usage Graph
* Disk Usage Graph
* Network Usage Graph

### User Interface

* Dark-themed dashboard
* Tab-based graph navigation
* Automatic updates every second
* Clean and responsive layout

---

## Technologies Used

* Python 3.x
* Tkinter (GUI)
* Psutil (System Monitoring)
* Matplotlib (Data Visualization)

---

## Project Structure

```
OS-Resource-Monitoring-Dashboard/
│
├── main.py
├── README.md
└── requirements.txt
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/OS-Resource-Monitoring-Dashboard.git
cd OS-Resource-Monitoring-Dashboard
```

### 2. Install Required Libraries

```bash
pip install psutil matplotlib
```

## Running the Application

Execute the following command:

```bash
python -m streamlit run main.py
```

## Dashboard Components

### Resource Information

* CPU Usage (%)
* Memory Usage (%)
* Disk Usage (%)
* Network Data Sent (MB)
* System Uptime
* Battery Percentage

### Process Monitor

Displays the top running processes based on CPU utilization.

### Performance Graphs

The dashboard continuously updates:

* CPU Usage Graph
* RAM Usage Graph
* Disk Usage Graph
* Network Activity Graph

---

## Future Enhancements

* GPU Monitoring
* Temperature Monitoring
* Export Reports to CSV/PDF
* Custom Alert Notifications
* Process Management (Kill Process Feature)
* Network Receive Statistics
* System Health Score

---

## Author

Developed as a system monitoring project using Python, Tkinter, Psutil, and Matplotlib.

---

## License

This project is open-source and available under the MIT License.
