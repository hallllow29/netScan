from scanner import scan_network, display_devices

def main_menu():

    print("Welcome to NetScan")
    print("Please choose an option: ")
    print("[1] Network Scan ")
    print("[2] Port Scan ")

    x = input("Option: ")

    if x == "1":
        ip_range = input("Enter a valid IP range (example: 192.168.1.0/24): ")
        scan_network(ip_range)

if __name__ == '__main__':
    main_menu()