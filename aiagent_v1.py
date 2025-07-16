import paramiko
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

#  Tool: Run Linux Command via SSH
@tool
def run_remote_linux_command(host: str, username: str, password: str, command: str = "uname -a") -> str:
    """Runs a Linux command on a remote machine via SSH."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        ssh.close()
        return f" Linux Output:\n{out}" if not err else f" Error:\n{err}"
    except Exception as e:
        return f" SSH Connection Error:\n{str(e)}"

# Tool: Run Docker Command via SSH
@tool
def run_remote_docker_command(host: str, username: str, password: str, command: str = "docker ps") -> str:
    """Runs a Docker command on a remote machine via SSH."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        ssh.close()
        return f" Docker Output:\n{out}" if not err else f" Docker Error:\n{err}"
    except Exception as e:
        return f"SSH Connection Error:\n{str(e)}"

#  Tool: Launch a Docker Container via SSH
@tool
def launch_docker_container(host: str, username: str, password: str, image: str = "ubuntu", name: str = "my_container") -> str:
    """Launches a Docker container remotely."""
    command = f"docker run -dit --name {name} {image} /bin/bash"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode().strip()
        err = stderr.read().decode()
        ssh.close()
        return f" Launched `{name}` using `{image}`.\nContainer ID: {out}" if not err else f" Error:\n{err}"
    except Exception as e:
        return f" SSH Launch Error:\n{str(e)}"

#  Gemini + LangGraph Agent
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyBJ1IX2NaFdULhgJxkmIIYfDghiIOpdryU", 
    convert_system_message_to_human=True,
    temperature=0.7
)

tools = [
    run_remote_linux_command,
    run_remote_docker_command,
    launch_docker_container
]

agent = create_react_agent(llm, tools)

#  Ask for SSH Credentials Once
host = input(" Enter SSH IP/Hostname: ")
username = input(" Enter SSH Username: ")
password = input(" Enter SSH Password: ")

#  Loop for Multiple Commands
print("\n Session ready! Type queries or 'exit' to quit.\n")
while True:
    query = input(" Enter your query (e.g. launch Docker, run Linux cmd): ")
    if query.strip().lower() == "exit":
        print(" Session ended.")
        break

    # Inject credentials & task into message
    user_content = (
        f"Log into {host} via SSH using username `{username}` and password `{password}`. "
        f"{query}"
    )

    input_message = {
        "role": "user",
        "content": user_content
    }

    for step in agent.stream({"messages": [input_message]}, stream_mode="values"):
        step["messages"][-1].pretty_print()