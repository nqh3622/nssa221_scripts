#!/usr/bin/env python3

import subprocess
import socket
import sys

def display_menu():
    print("\n=== Network Diagnostic Menu ===")
    print("1. Display the Default Gateway")
    print("2. Test Local Connectivity")
    print("3. Test Remote Connectivity")
    print("4. Test DNS Resolution")
    print("5. Exit\n")

def get_default_gateway():
    try:
        print("\nDefault Gateway:")
        result = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve default gateway.")

def test_local_connectivity():
    print("\nTesting local connectivity (ping to 127.0.0.1)...")
    try:
        subprocess.run(["ping", "-c", "4", "127.0.0.1"], check=True)
    except subprocess.CalledProcessError:
        print("Local connectivity test failed.")

def test_remote_connectivity():
    print("\nTesting remote connectivity (ping to 8.8.8.8)...")
    try:
        subprocess.run(["ping", "-c", "4", "8.8.8.8"], check=True)
    except subprocess.CalledProcessError:
        print("Remote connectivity test failed. Please check your network connection.")

def test_dns_resolution():
    test_domain = "www.google.com"
    print(f"\nTesting DNS resolution for {test_domain}...")
    try:
        ip = socket.gethostbyname(test_domain)
        print(f"DNS Resolution successful: {test_domain} -> {ip}")
    except socket.gaierror:
        print("DNS resolution failed. Check your DNS settings.")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            get_default_gateway()
        elif choice == "2":
            test_local_connectivity()
        elif choice == "3":
            test_remote_connectivity()
        elif choice == "4":
            test_dns_resolution()
        elif choice == "5":
            print("Exiting script.")
            sys.exit(0)
        else:
            print("Invalid selection. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
