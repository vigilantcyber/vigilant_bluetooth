import time
import os
import subprocess

def print_logo():
    print("My Bluetooth Management Tool")

def _kick_(mac_address, duration, intensity, start_time):
    print(f"Kicking Bluetooth device with MAC address {mac_address} in {start_time} seconds.")
    time.sleep(start_time)
    try:
        # Disconnect the Bluetooth device
        subprocess.run(["bluetoothctl", "disconnect", mac_address], check=True)
        print(f"Device {mac_address} kicked for {duration} seconds with intensity {intensity}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to kick device: {e}")

def scan_for_bluetooth_devices():
    print("Scanning for Bluetooth devices...")
    devices = []
    
    try:
        # Run a Bluetooth scan
        result = subprocess.run(["bluetoothctl", "scan", "on"], capture_output=True, text=True)
        time.sleep(10)  # Allow some time for the scan
        subprocess.run(["bluetoothctl", "scan", "off"], check=True)

        # Process scan output to extract MAC addresses
        output = result.stdout
        lines = output.split('\n')
        for line in lines:
            if "Device" in line:
                parts = line.split()
                if len(parts) > 1:
                    devices.append(parts[1])
    
    except subprocess.CalledProcessError as e:
        print(f"Scanning failed: {e}")

    if devices:
        print("Found devices:")
        for i, device in enumerate(devices):
            print(f"{i + 1}: {device}")
        selected_index = int(input("Select a device by number: ")) - 1
        if 0 <= selected_index < len(devices):
            return devices[selected_index]
        else:
            print("Invalid selection.")
            return None
    else:
        print("No devices found.")
        return None

def get_valid_integer(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def main_modules():
    print_logo()
    
    modules = """1 :mag: Scan for Bluetooth Devices
2 :satellite: Kick Out Bluetooth Devices
Q :door: Exit (Ctrl + C)"""
    
    print(modules)
    
    user_choice = input("Enter your choice: ").strip()
    
    if user_choice == "1":
        mac_address = scan_for_bluetooth_devices()
        if mac_address:
            print(f"Selected MAC address: {mac_address}")
            
            while True:
                scan_again = input("Do you want to perform the scan again (y/n)? ").strip().lower()
                if scan_again == "y":
                    mac_address = scan_for_bluetooth_devices()
                    if mac_address:
                        print(f"Selected MAC address: {mac_address}")
                elif scan_again == "n":
                    break
                else:
                    print("Invalid option. Please enter 'y' or 'n'.")
            
            kick_ard = input("Do you want to kick the user (y/n)? ").strip().lower() == "y"
            if kick_ard:
                start_time = get_valid_integer("In how many seconds do you want to start the attack? ")
                _kick_(mac_address, 600, 10, start_time)
            else:
                print("Exiting...")
    
    elif user_choice == "2":
        mac_address = input("Enter the MAC address: ").strip()
        start_time = get_valid_integer("In how many seconds do you want to start the attack? ")
        _kick_(mac_address, 600, 20, start_time)
        
    elif user_choice.lower() == "q":
        print("Exiting...")
        exit()
    
    else:
        print("Invalid option")
        time.sleep(1)
        main_modules()

if __name__ == "__main__":
    try:
        # Turns Bluetooth Adapter - ON
        os.system("rfkill unblock bluetooth")
        # ----------------------------------
        main_modules()
    except KeyboardInterrupt:
        print("User Quit")
        exit()
    except Exception as e:
        print(f"ERROR: {e}")
        exit()
