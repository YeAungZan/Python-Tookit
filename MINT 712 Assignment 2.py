# Import required modules
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import subprocess

# Ask the user for a username when the program starts
username = input("Enter username: ")
print(f"\nWelcome to the Toolkit program, {username}!")

# Main function that starts the program
def main():
    menu()

# Displays the toolkit menu and allows the user to select utilities
def menu():
    while True:
        print("\n****** Toolkit menu ******\n")
        print("Please select a utility from the menu below:")
        print("1. Port scanner")
        print("2. Udp ping")
        print("3. ICMP traceroute")
        print("4. Under development")
        print("5. Under development")
        print("6. Exit")

        # Get user menu choice
        choice = input("Please enter utility you want to use: ")

        # Call the corresponding function depending on the user choice
        if choice == '1':
            port_scanner()
        elif choice == '2':
            udp_ping()
        elif choice == '3':
            icmp_traceroute()
        elif choice == '4':
            print("Under development!")
        elif choice == '5':
            print("Under development!")
        elif choice == '6':
            print("Exiting the menu. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
            menu()

# Function that performs TCP port scanning
def port_scanner():
    # Ask user for starting and ending target IP addresses
    Starting_target_host = input("Enter the target host: ")
    Ending_target_host = input("Enter the ending target host: ")

    # Ask for starting port
    start_port = int(input("Enter starting TCP port: "))

    # If the starting port is 0, scan all ports
    if start_port == 0:
        starting_port_no = 1
        ending_port_no = 65535
    else:
        # Ask for ending port
        end_port = input("Enter ending TCP port: ")
        # If it is blank, scan only the starting port
        if end_port.strip() == "":
            starting_port_no = start_port
            ending_port_no = start_port
        else:
            starting_port_no = start_port
            ending_port_no = int(end_port)

# Function that scans a single port on a host
    def scan_port(current_host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            # connect_ex returns 0 if connection is successful
            connect = s.connect_ex((current_host, port))

            if connect == 0:
                print(f"IP address: {current_host}, Port {port} is open")

            s.close()
        except:
            pass
    

    # Function that scans all ports of a specific host using threads
    def scan_host(current_host):
        # Thread pool allows multiple ports to be scanned simultaneously
        with ThreadPoolExecutor(max_workers=5) as executor:
            for port in range(starting_port_no, ending_port_no + 1):
                executor.submit(scan_port, current_host, port)

    # If a range of hosts is provided, scan each host
    if Ending_target_host.strip() != "":
        for host in range(
            int(Starting_target_host.split(".")[-1]),
            int(Ending_target_host.split(".")[-1]) + 1 ):
            current_host = ".".join(Starting_target_host.split(".")[:-1]) + "." + str(host)
            scan_host(current_host)
    else:
        scan_host(Starting_target_host)

# Function that performs UDP ping
def udp_ping():
    host = input("Enter IP Address to ping: ")
    port = 12345  
    name = "YeAungZan"  
    name_bytes = name.encode()

    # Building 56 bytes payload
    buffer_size = 56 - len(name_bytes)
    payload = name_bytes + b' ' * buffer_size

    print(f"\nPinging {host} with 56 bytes of data:\n")

    # Initialize counters for sent packets, received packets, and list to store RTT values
    sent = 0
    received = 0
    rtt_list = []
    
    # Send 5 ping packets
    for i in range(5):
        # Create UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)

        try:
            start = time.time()
            s.sendto(payload, (host, port))
            sent += 1

            data, addr = s.recvfrom(1024)
            end = time.time()

            # Calculate RTT in milliseconds
            rtt = int((end - start) * 1000)  
            rtt_list.append(rtt)
            received += 1

            ttl = 119  
            print(f"Reply from {host}: bytes=56 time={rtt}ms TTL={ttl}")

        except socket.timeout:
            sent += 1
            print("Request timed out.")

        s.close()
        time.sleep(1)

    # Calculate packet loss
    lost = sent - received
    loss_percent = int((lost / sent) * 100)

    print(f"\nPing statistics for {host}:")
    print(f"Packets: Sent = {sent}, Received = {received}, Lost = {lost} ({loss_percent}% loss)")

    # Calculate RTT statistics
    if received > 0:
        minimum = min(rtt_list)
        maximum = max(rtt_list)
        average = int(sum(rtt_list) / len(rtt_list))

        print("Approximate round trip times in milli-seconds:")
        print(f"Minimum = {minimum}ms, Maximum = {maximum}ms, Average = {average}ms")

# Function that performs ICMP traceroute
def icmp_traceroute():
    host = input("Enter target hosts: ")
    print(f"\nTraceroute to {host}\n")

    # Call system traceroute command with ICMP option
    subprocess.call(["traceroute", "-I", host])
    print()

main()

