# src/tools/system_monitor.py

import psutil
from datetime import datetime

def get_system_report():
    """Get PC health metrics"""
    
    # Get CPU usage
    cpu = psutil.cpu_percent(interval=1)
    
    # Get memory info
    memory = psutil.virtual_memory()
    mem_used = round(memory.used / (1024**3), 1)  # GB
    mem_total = round(memory.total / (1024**3), 1)  # GB
    mem_percent = memory.percent
    
    # Get disk info
    disk = psutil.disk_usage('/')
    disk_used = round(disk.used / (1024**3), 1)  # GB
    disk_total = round(disk.total / (1024**3), 1)  # GB
    disk_percent = disk.percent
    
    # Create report
    report = f"""
PC Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CPU Usage: {cpu}%
Memory: {mem_used} GB / {mem_total} GB ({mem_percent}%)
Disk: {disk_used} GB / {disk_total} GB ({disk_percent}%)
"""
    
    return report.strip()

# Test it
if __name__ == "__main__":
    print("\n" + "="*50)
    print("System Monitor Test")
    print("="*50 + "\n")
    
    report = get_system_report()
    print(report)
    
    print("\n" + "="*50)
    print("✅ System monitor working!")
    print("="*50 + "\n")
