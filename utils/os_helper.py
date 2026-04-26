import platform

def detect_os():
    system = platform.system().lower()
    if "windows" in system:
        return "Windows"
    if "darwin" in system:
        return "macOS"
    if "linux" in system:
        return "Linux"
    return "Unknown"
