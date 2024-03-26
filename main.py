import udp
import tcp
import threading

if __name__ == "__main__":
    udp = udp.UDP_discovery("zabransky_peer1", "0.0.0.0", "172.31.255.255", 9876)

    tcp = tcp.TCP_Communication("zabransky_peer1", "172.24.13.3", 9876)

    try:
        send_thread = threading.Thread(target=udp.send_discovery_message)
        receive_thread = threading.Thread(target=udp.receive_responses)
        tcp_thread = threading.Thread(target=tcp.communicate_with_peer)

        send_thread.start()
        receive_thread.start()
        tcp_thread.start()

        send_thread.join()
        receive_thread.join()
        tcp_thread.join()
    except KeyboardInterrupt:
        print("Stopping the discovery and communication service.")
    
