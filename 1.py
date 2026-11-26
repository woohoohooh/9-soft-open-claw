
from pathlib import Path
import subprocess

ROOT = Path.home() / ".openclaw"
VBS_FILE = ROOT / "gateway-hidden.vbs"
GATEWAY_CMD = ROOT / "gateway.cmd"

if not GATEWAY_CMD.exists():
    raise FileNotFoundError(f"Gateway not found: {GATEWAY_CMD}")

vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "{ROOT}"
WshShell.Run """{GATEWAY_CMD}""", 0, False
'''

VBS_FILE.write_text(vbs_content, encoding="utf-8")

powershell = f'''
$action = New-ScheduledTaskAction `
    -Execute "wscript.exe" `
    -Argument '"{VBS_FILE}"'

Set-ScheduledTask -TaskName "OpenClaw Gateway" -Action $action
'''

result = subprocess.run(
    ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("ERROR:")
    print(result.stderr)
else:
    print("SUCCESS!")
    print(f"Created: {VBS_FILE}")
    print("OpenClaw Gateway task updated.")
    print("Gateway will now launch without a visible terminal window.")
