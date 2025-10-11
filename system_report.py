#!/usr/bin/env python3

#Nathaniel Hartley
#10/9/25

import os
import platform
import subprocess
from datetime import datetime
import socket

#run_command method takes in a command in the form of a string and uses the subprocess module to run the command
#returns the string result with the leading and trailing whitespace trimmed.

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

#get_hostname calls on the socket module and returns the hostname of the machine as a string

def get_hostname():
    return socket.gethostname()

#get_domain calls on the run_command method with a the linux command to retreive the hostname
#it returns the result if a result is given, or "N/A" if no hostname exists

def get_domain():
    if run_command("hostname -d").__len__() != 0:
        return run_command("hostname -d")
    else:
        return "N/A"
    
#get_ip_address runs a linux command which returns the systems network interface ip address
#it returns the output if an address is present, or "N/A" if no ip address exists

def get_ip_address():
    output = run_command("hostname -I")
    if output.__len__ != 0:
        return output
    else:
        return "N/A"
    
#get_gateway runs a linux command which returns the systems gateway ip address
#it splits the output into a list of strings and then if the list is greater than or equal to 3, it returns the 2nd index of the list
#else it returns "N/A"

def get_gateway():
    output = run_command("ip route | grep default")
    parts = output.split()
    if len(parts) >= 3:
        return parts[2]
    else:
        return "N/A"

#get_netmask runs a linux command for the system's network interface IP address
#if the address exists, it calculates what the netmask would be based on the address

def get_netmask():
    output = run_command("hostname -I")
    if output:
        cidr = output.__len__()
        mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
        return '.'.join([str((mask >> (i * 8)) & 0xff) for i in [3, 2, 1, 0]])
    return "N/A"

#get_dns creates an empty list called dns_lines, opens a file and proceeds to line by line in the file. 
#If the line line starts with "nameserver", the line is stripped of whitespace, split into a list, and the 1st index is appended to the dns_lines list.
#Error handling is in place beacuse this whole file reading section is enclosed in a try block, if it fails for any reason, the dns_lines list is set to "N/A"

def get_dns():
    dns_lines = []
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns_lines.append(line.strip().split()[1])
    except:
        dns_lines = ["N/A"]
    if dns_lines:
        return dns_lines
    else:
        return ["N/A"]
    
#get_os_info checks to see if the platform has the given name of "linux_distribution, if it does it returns the platform module
#if it doesn't, it returns the result of running the linux command to print the redhat_release file

def get_os_info():
    if hasattr(platform, 'linux_distribution'):
        return platform.linux_distribution()
    else:
        return run_command("cat /etc/redhat-release")

#get_kernal_version returns the version number as a string throught the platform module

def get_kernel_version():
    return platform.release()

#get_disk_info runs the linux command for showing the drives existing on a particular linux device. 
#the output of the command is split into a list, and if that list has a length greater than or equal to 2, data from the list of lines is saved into variables
#these variables reprsent the total space, the used space and the free space on a particular drive

def get_disk_info():
    output = run_command("df -h /")
    lines = output.splitlines()
    if len(lines) >= 2:
        columns = lines[1].split()
        total = columns[1]
        used = columns[2]
        free = columns[3]
        return total, used, free
    return "N/A", "N/A", "N/A"

#get_cpu_info calls on the run_command method to grep a series of details about the model, cores and number of processors
#this info is then stripped and or split to retrieve the specified information from the long output and returned

def get_cpu_info():
    model = run_command("grep 'model name' /proc/cpuinfo | head -1").split(":")[1].strip()
    processors = run_command("grep 'physical id' /proc/cpuinfo | sort -u | wc -l").strip()
    cores = run_command("grep -c ^processor /proc/cpuinfo").strip()
    return model, processors, cores

#get_memory_info calls on the run_command method and splits the output into a list of strings.
#if the lines have a length of greater than or equal to 2, the line is split, and the first and the last index of is saved and returned.

def get_memory_info():
    output = run_command("free -h")
    lines = output.splitlines()
    if len(lines) >= 2:
        mem_line = lines[1].split()
        total = mem_line[1]
        available = mem_line[-1]
        return total, available
    return "N/A", "N/A"

#method which creates and formats the output to the user.

def create_report():
    hostname = get_hostname()
    domain = get_domain()
    ip = get_ip_address()
    gateway = get_gateway()
    netmask = get_netmask()
    dns_servers = get_dns()
    os_info = get_os_info()
    kernel_version = get_kernel_version()
    disk_total, disk_used, disk_free = get_disk_info()
    cpu_model, cpu_processors, cpu_cores = get_cpu_info()
    mem_total, mem_available = get_memory_info()
    date_str = datetime.now().strftime("%B %d, %Y")

    report = f"""
\033[1;31mSystem Report\033[0m - {date_str}

\033[1;32mDevice Information\033[0m
Hostname:           {hostname}
Domain:             {domain}

\033[1;32mNetwork Information\033[0m
IP Address:         {ip}
Gateway:            {gateway}
Network Mask:       {netmask}
DNS1:               {dns_servers[0] if len(dns_servers) > 0 else 'N/A'}
DNS2:               {dns_servers[1] if len(dns_servers) > 1 else 'N/A'}

\033[1;32mOperating System Information\033[0m
Operating System:   {os_info}
OS Version:         {platform.release()}
Kernel Version:     {kernel_version}

\033[1;32mStorage Information\033[0m
System Drive Total: {disk_total}
System Drive Used:  {disk_used}
System Drive Free:  {disk_free}

\033[1;32mProcessor Information\033[0m
CPU Model:          {cpu_model}
Number of processors: {cpu_processors}
Number of cores:    {cpu_cores}

\033[1;32mMemory Information\033[0m
Total RAM:          {mem_total}
Available RAM:      {mem_available}
"""
    return report.strip()

#this method takes in the output shown the user and the user's hostname and creates a logfile. 
#A message is then outputted to the user that the file has been saved.

def save_to_logfile(report, hostname):
    logfile = os.path.join(os.path.expanduser("~"), f"{hostname}_system_report.log")
    with open(logfile, "w") as log:
        log.write(report.replace("\033[1;31m", "")
                        .replace("\033[1;32m", "")
                        .replace("\033[0m", ""))
    print(f"\nLog file saved to {logfile}")

def main():
    hostname = get_hostname()
    report = create_report()
    print(report)
    save_to_logfile(report, hostname)

if __name__ == "__main__":
    main()

