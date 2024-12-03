import time
import os
import subprocess
import re

def print_logo():
    print("My Bluetooth Management Tool")

def execute_bluetoothctl_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}")
        return None

def scan_for_bluetooth_devices():
    print("Scanning for Bluetooth devices...")
    try:
        # Start scanning
        execute_bluetoothctl_command(["bluetoothctl", "scan", "on"])
        time.sleep(10)  # Allow time for devices to be discovered
        
        # Stop scanning
        scan_output = execute_bluetoothctl_command(["bluetoothctl", "scan", "off"])
        if not scan_output:
            print("No devices found.")
            return None
        
        # Extract the first detected device
        for line in scan_output.split('\n'):
            if "Device" in line:
                parts = line.split()
                if len(parts) > 1 and re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', parts[1], re.I):
                    mac_address = parts[1]
                    device_name = ' '.join(parts[2:])
                    print(f"Auto-captured device: {mac_address} ({device_name})")
                    return mac_address
        
        print("No valid devices found.")
    except Exception as e:
        print(f"Error during scanning: {e}")
    return None

def kick_device(mac_address, duration, start_time):
    if not re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', mac_address, re.I):
        print("Invalid MAC address format.")
        return
    print(f"Kicking Bluetooth device {mac_address} in {start_time} seconds for {duration} seconds...")
    time.sleep(start_time)
    try:
        execute_bluetoothctl_command(["bluetoothctl", "disconnect", mac_address])
        print(f"Device {mac_address} has been disconnected.")
    except Exception as e:
        print(f"Failed to disconnect device: {e}")

def get_valid_integer(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def main_menu():
    print_logo()
    while True:
        print("""
        1: Scan and Auto-Capture Bluetooth Device
        2: Kick Out Bluetooth Device
        Q: Exit
        """)
        choice = input("Enter your choice: ").strip().lower()
        if choice == '1':
            mac = scan_for_bluetooth_devices()
            if mac:
                print(f"Auto-captured device: {mac}")
        elif choice == '2':
            mac = input("Enter the MAC address: ").strip()
            start_time = get_valid_integer("Enter the delay before kicking (in seconds): ")
            kick_device(mac, duration=600, start_time=start_time)
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    try:
        os.system("rfkill unblock bluetooth")
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except Exception as e:
        print(f"Unexpected error: {e}")
