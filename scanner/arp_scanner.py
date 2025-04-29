import scapy.all as scapy

def scan (ip_range):
    print(f"Scanning IP range: {ip_range}")

    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    print("Sending ARP requests...")
    answered_list = scapy.srp(arp_request_broadcast, timeout = 5, verbose = True) [0]

    if not answered_list:
        print ("No response received")
    else:
        print ("Responses received")

    devices =  []
    for element in answered_list:
        device = {'ip':element[1].psrc, 'mac': element[1].hwsrc}
        devices.append(device)
        print(f"Device found: IP = {device['ip']}, MAC = {device['mac']}")

    return devices

def display_devices(devices):
    if devices:
        print("\nIP\t\t\tMAC Address")
        print("-----------------------------------------")
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")
    else:
        print("No devices found.")

def scan_network(ip_range):
    devices = scan(ip_range)
    display_devices(devices)

