import streamlit as st
import psutil
import pandas as pd
import plotly.graph_objects as go
import time
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="OS Resource Monitoring Dashboard",
    page_icon="🖥️",
    layout="wide"
)

st_autorefresh(interval=2000, key="refresh")

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
    background-color:#f5f7fa;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    text-align:center;
}

.metric-title{
    color:#6b7280;
    font-size:14px;
}

.metric-value{
    color:#111827;
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🖥️ OS Resource Monitoring Dashboard")
st.caption("Real-Time System Monitoring")

# ---------------- SESSION STATE ----------------

for key in ["cpu_hist", "ram_hist", "disk_hist", "net_hist"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------- SYSTEM DATA ----------------

cpu = psutil.cpu_percent()

memory = psutil.virtual_memory()
ram = memory.percent

disk = psutil.disk_usage("/").percent

network = psutil.net_io_counters()
sent = network.bytes_sent / (1024 * 1024)

battery = psutil.sensors_battery()

if battery:
    battery_text = f"{battery.percent}%"
else:
    battery_text = "--"

boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time

hours = int(uptime_seconds // 3600)
minutes = int((uptime_seconds % 3600) // 60)

# ---------------- KPI CARDS ----------------

c1, c2, c3, c4, c5, c6 = st.columns(6)

cards = [
    ("CPU", f"{cpu}%"),
    ("RAM", f"{ram}%"),
    ("DISK", f"{disk}%"),
    ("NETWORK", f"{sent:.2f} MB"),
    ("BATTERY", battery_text),
    ("UPTIME", f"{hours}h {minutes}m")
]

for col, (title, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        cards):

    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- STORE HISTORY ----------------

st.session_state.cpu_hist.append(cpu)
st.session_state.ram_hist.append(ram)
st.session_state.disk_hist.append(disk)
st.session_state.net_hist.append(sent)

if len(st.session_state.cpu_hist) > 20:
    st.session_state.cpu_hist.pop(0)
    st.session_state.ram_hist.pop(0)
    st.session_state.disk_hist.pop(0)
    st.session_state.net_hist.pop(0)

# ---------------- CHARTS ----------------

st.subheader("📈 Resource Trends")

tab1, tab2, tab3, tab4 = st.tabs(
    ["CPU", "RAM", "Disk", "Network"]
)

with tab1:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=st.session_state.cpu_hist,
        mode="lines+markers",
        name="CPU"
    ))

    fig.update_layout(
        template="plotly_white",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=st.session_state.ram_hist,
        mode="lines+markers",
        name="RAM"
    ))

    fig.update_layout(
        template="plotly_white",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=st.session_state.disk_hist,
        mode="lines+markers",
        name="Disk"
    ))

    fig.update_layout(
        template="plotly_white",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=st.session_state.net_hist,
        mode="lines+markers",
        name="Network"
    ))

    fig.update_layout(
        template="plotly_white",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TOP PROCESSES ----------------

st.subheader("⚙️ Top Running Processes")

processes = []

for proc in psutil.process_iter(
        ['pid', 'name', 'cpu_percent']):
    try:
        processes.append([
            proc.info['name'],
            proc.info['pid'],
            proc.info['cpu_percent']
        ])
    except:
        pass

process_df = pd.DataFrame(
    processes,
    columns=[
        "Process Name",
        "PID",
        "CPU %"
    ]
)

process_df = process_df.sort_values(
    by="CPU %",
    ascending=False
).head(10)

st.dataframe(
    process_df,
    use_container_width=True
)

# ---------------- DOWNLOAD REPORT ----------------

report_df = pd.DataFrame({
    "CPU":[cpu],
    "RAM":[ram],
    "DISK":[disk],
    "NETWORK_MB":[round(sent,2)]
})

st.download_button(
    "📥 Download Report",
    report_df.to_csv(index=False),
    file_name="system_report.csv"
)