import streamlit as st
import paramiko
import speech_recognition as sr
import threading
from functools import wraps
import warnings

# Suppress paramiko deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# -------- SSH Client Setup --------
def get_ssh_client(host, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)
        return client
    except Exception as e:
        st.error(f"SSH connection failed: {e}")
        return None

# -------- Decorator & Registry --------
COMMAND_REGISTRY = {}

def register_command(label, description=""):
    def decorator(func):
        COMMAND_REGISTRY[label] = {"func": func, "description": description}
        @wraps(func)
        def wrapper(client):
            return func(client)
        return wrapper
    return decorator

# -------- SSH Command Executor --------
def run_command(client, cmd):
    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output or error
    except Exception as e:
        return f"Error: {e}"

# -------- Speech Recognition --------
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        st.error("Could not understand your voice.")
        return ""

# -------- Register Commands --------
@register_command("1. List Files", "Lists all files and directories with details.")
def cmd1(c): return run_command(c, "ls -al")

@register_command("2. Present Directory", "Displays the current working directory.")
def cmd2(c): return run_command(c, "pwd")

@register_command("3. Disk Space", "Shows disk space usage.")
def cmd3(c): return run_command(c, "df -h")

@register_command("4. Free Memory", "Displays free and used memory.")
def cmd4(c): return run_command(c, "free -m")

@register_command("5. System Uptime", "Shows how long the system has been running.")
def cmd5(c): return run_command(c, "uptime")

@register_command("6. CPU Info", "Displays CPU architecture details.")
def cmd6(c): return run_command(c, "lscpu")

@register_command("7. RAM Info", "Shows RAM usage and memory info.")
def cmd7(c): return run_command(c, "cat /proc/meminfo")

@register_command("8. Kernel Version", "Displays the Linux kernel version.")
def cmd8(c): return run_command(c, "uname -r")

@register_command("9. OS Release Info", "Shows the OS release information.")
def cmd9(c): return run_command(c, "cat /etc/os-release")

@register_command("10. Whoami", "Displays current user.")
def cmd10(c): return run_command(c, "whoami")

@register_command("11. Hostname", "Displays the system's hostname.")
def cmd11(c): return run_command(c, "hostname")

@register_command("12. IP Address", "Shows the IP address of the machine.")
def cmd12(c): return run_command(c, "hostname -I")

@register_command("13. Logged-in Users", "Displays users currently logged in.")
def cmd13(c): return run_command(c, "w")

@register_command("14. All Users", "Lists all users of the system.")
def cmd14(c): return run_command(c, "cut -d: -f1 /etc/passwd")

@register_command("15. Network Interfaces", "Displays network interface details.")
def cmd15(c): return run_command(c, "ip a")

@register_command("16. Ping Google", "Checks network connectivity to Google.")
def cmd16(c): return run_command(c, "ping -c 3 google.com")

@register_command("17. Open Ports", "Lists open network ports.")
def cmd17(c): return run_command(c, "sudo netstat -tuln")

@register_command("18. Recent Logins", "Shows recent login history.")
def cmd18(c): return run_command(c, "last -n 5")

@register_command("19. Top Processes", "Displays top memory-consuming processes.")
def cmd19(c): return run_command(c, "ps aux --sort=-%mem | head")

@register_command("20. Disk Partitions", "Shows disk partition layout.")
def cmd20(c): return run_command(c, "lsblk")

@register_command("21. Tree View", "Lists directory structure.")
def cmd21(c): return run_command(c, "tree -L 1")

@register_command("22. Environment Variables", "Displays system environment variables.")
def cmd22(c): return run_command(c, "printenv")

@register_command("23. Firewall Status", "Shows current firewall status.")
def cmd23(c): return run_command(c, "sudo ufw status")

@register_command("24. Installed Packages", "Lists recently installed packages.")
def cmd24(c): return run_command(c, "dpkg -l | head -15")

@register_command("25. Running Services", "Lists currently running services.")
def cmd25(c): return run_command(c, "systemctl list-units --type=service --state=running")

@register_command("26. SSH Sessions", "Shows active SSH sessions.")
def cmd26(c): return run_command(c, "who | grep ssh")

@register_command("27. Mount Points", "Displays mounted drives and paths.")
def cmd27(c): return run_command(c, "mount | head -10")

@register_command("28. CPU Usage Snapshot", "Shows a snapshot of CPU usage.")
def cmd28(c): return run_command(c, "top -b -n1 | head -20")

@register_command("29. Cron Jobs", "Displays current user's cron jobs.")
def cmd29(c): return run_command(c, "crontab -l")

@register_command("30. Help Summary", "Summary of common commands you can try.")
def cmd30(c): return "Try commands like 'disk space', 'cpu info', 'uptime', etc."

# -------- Streamlit UI --------
st.set_page_config("Linux SSH Dashboard", layout="wide")
st.markdown("""
<style>
.stButton > button {
    background-color: #2d2d2d;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5em 1em;
}
.stExpanderHeader {
    font-size: 1.1em;
    color: #2a2a2a;
}
</style>
""", unsafe_allow_html=True)

st.title("🐧 Linux SSH Dashboard")
st.markdown("Manage your remote Linux system from Windows via *SSH*, using voice or press input.")

# SSH Sidebar
with st.sidebar:
    st.header("🔐 SSH Login")
    host = st.text_input("Host")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Connect"):
        ssh = get_ssh_client(host, user, password)
        if ssh:
            st.session_state['ssh'] = ssh
            st.success("✅ Connected to server!")

    if 'ssh' in st.session_state:
        st.sidebar.success("🟢 Connected")
        st.sidebar.markdown(f"**Host:** {host}  \n**User:** {user}")
        if st.button("Disconnect"):
            st.session_state['ssh'].close()
            del st.session_state['ssh']
            st.sidebar.success("🔌 Disconnected successfully.")

# Command Input
if 'ssh' in st.session_state:
    ssh = st.session_state['ssh']
    input_mode = st.radio("Choose Input Mode", ["Press", "Voice"], horizontal=True)

    if input_mode == "Press":
        st.subheader("📋 Select a Command")
        cols = st.columns(3)
        for i, (label, meta) in enumerate(COMMAND_REGISTRY.items()):
            with cols[i % 3].expander(label):
                st.markdown(f"**Description:** {meta['description']}")
                if st.button(f"▶️ Run {label}", key=label):
                    output = meta['func'](ssh)
                    st.code(output, language="bash")

    elif input_mode == "Voice":
        st.subheader("🎙 Voice Command Input")
        st.markdown("_Say things like **disk space**, **whoami**, **cpu info**..._")
        if st.button("Start Listening"):
            def process_voice():
                query = recognize_speech()
                for label, meta in COMMAND_REGISTRY.items():
                    phrase = label.split(". ", 1)[-1].lower()
                    if phrase in query:
                        st.success(f"Running: {label}")
                        result = meta['func'](ssh)
                        st.code(result, language="bash")
                        return
                st.warning("No matching command found.")
            threading.Thread(target=process_voice).start()