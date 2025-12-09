import socket
import threading
import json

# ----------------------------
# Server configuration
# ----------------------------
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5000  # Port for TCP connections

# ----------------------------
# Vehicle Manager
# ----------------------------
vehicles = {}  # Dictionary to store vehicle info {vehicle_id: info}


# ----------------------------
# Handle each client connection
# ----------------------------
def handle_client(conn, addr):
    print(f"[CONNECTED] {addr} connected.")
    try:
        while True:
            data = conn.recv(1024)  # Receive up to 1024 bytes
            if not data:
                break  # Client disconnected

            # Decode bytes to string
            message = data.decode('utf-8')

            try:
                # Parse JSON
                vehicle_data = json.loads(message)
                vehicle_id = vehicle_data.get("vehicle_id")
                print(f"[RECEIVED] Vehicle: {vehicle_id} from {addr}")

                # Store/update vehicle info
                vehicles[vehicle_id] = vehicle_data

                # Respond back
                response = {"status": "received", "vehicle_id": vehicle_id}
                conn.sendall(json.dumps(response).encode('utf-8'))

            except json.JSONDecodeError:
                print("[ERROR] Invalid JSON received")
                conn.sendall(b'{"status":"error","message":"invalid json"}')

    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")


# ----------------------------
# Main server loop
# ----------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


# ----------------------------
# Run the server
# ----------------------------
if __name__ == "__main__":
    start_server()
