import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import subprocess

print("Welcome to the program!")

def main():
    menu()

def menu():
    while True:
        print("\n****** Welcome to the menu! ******")
        print("1. Port scanner")
        print("2. Udp ping")
        print("3. ICMP traceroute")
        print("4. Under development")
        print("5. Under development")
        print("6. Exit")

        choice = input("Please enter your choice: ")

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

def port_scanner():
    Starting_target_host = input("Enter the target host: ")
    Ending_target_host = input("Enter the ending target host: ")

    start_port = int(input("Enter starting TCP port: "))

    if start_port == 0:
        starting_port_no = 1
        ending_port_no = 65535
    else:
        end_port = input("Enter ending TCP port: ")
        if end_port.strip() == "":
            starting_port_no = start_port
            ending_port_no = start_port
        else:
            starting_port_no = start_port
            ending_port_no = int(end_port)

    def scan_port(current_host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            connect = s.connect_ex((current_host, port))

            if connect == 0:
                print(f"IP address: {current_host}, Port {port} is open")

            s.close()
        except:
            pass

    def scan_host(current_host):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for port in range(starting_port_no, ending_port_no + 1):
                executor.submit(scan_port, current_host, port)

    if Ending_target_host.strip() != "":
        for host in range(
            int(Starting_target_host.split(".")[-1]),
            int(Ending_target_host.split(".")[-1]) + 1
        ):
            current_host = ".".join(Starting_target_host.split(".")[:-1]) + "." + str(host)
            scan_host(current_host)
    else:
        scan_host(Starting_target_host)

def udp_ping():
    host = input("Enter IP Address to ping: ")
    port = 12345  # UDP port (server must be listening)

    # ---- Create 56-byte payload ----
    name = "YeAungZan"   # change to your first and last name
    name_bytes = name.encode()

    # Fill remaining bytes to make total 56 bytes
    buffer_size = 56 - len(name_bytes)
    payload = name_bytes + b' ' * buffer_size

    print(f"\nPinging {host} with 56 bytes of data:\n")

    sent = 0
    received = 0
    rtt_list = []

    for i in range(5):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)

        try:
            start = time.time()
            s.sendto(payload, (host, port))
            sent += 1

            data, addr = s.recvfrom(1024)
            end = time.time()

            rtt = int((end - start) * 1000)  # convert to ms
            rtt_list.append(rtt)
            received += 1

            ttl = 119  # simulated TTL (UDP does not provide TTL easily)
            print(f"Reply from {host}: bytes=56 time={rtt}ms TTL={ttl}")

        except socket.timeout:
            sent += 1
            print("Request timed out.")

        s.close()
        time.sleep(1)

    # ---- Statistics ----
    lost = sent - received
    loss_percent = int((lost / sent) * 100)

    print(f"\nPing statistics for {host}:")
    print(f"Packets: Sent = {sent}, Received = {received}, Lost = {lost} ({loss_percent}% loss)")

    if received > 0:
        minimum = min(rtt_list)
        maximum = max(rtt_list)
        average = int(sum(rtt_list) / len(rtt_list))

        print("Approximate round trip times in milli-seconds:")
        print(f"Minimum = {minimum}ms, Maximum = {maximum}ms, Average = {average}ms")


def icmp_traceroute():
    host = input("Enter target hosts: ")
    print(f"\nTraceroute to {host}\n")
    subprocess.call(["traceroute", "-I", host])
    print()

if __name__ == "__main__":
    main()

