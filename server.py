import socket
import threading
import json
import os

HOST = 'localhost'
PORT = 12345

# Create initial database file if not exists
if not os.path.exists("database.json"):
    with open("database.json", "w") as f:
        json.dump({
            "users": [{"username": "admin", "password": "admin"}],
            "patients": [],
            "appointments": []
        }, f)

def handle_client(conn, addr):
    print(f"Connected to {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("Received:", data)  # Debug
            response = handle_request(data)
            conn.sendall(response.encode())
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def handle_request(data):
    try:
        parts = data.strip().split("|")
        command = parts[0]
    except Exception as e:
        return f"ERROR: Failed to parse request - {e}"

    # Load database
    with open("database.json", "r") as f:
        db = json.load(f)

    if command == "LOGIN":
        username, password = parts[1], parts[2]
        for user in db["users"]:
            if user["username"] == username and user["password"] == password:
                return "LOGIN_SUCCESS"
        return "LOGIN_FAILED"

    elif command == "REGISTER_PATIENT":
        patient = {
            "name": parts[1],
            "age": parts[2],
            "gender": parts[3],
            "id": len(db["patients"]) + 1
        }
        db["patients"].append(patient)

    elif command == "BOOK_APPOINTMENT":
        appointment = {
            "patient_id": parts[1],
            "doctor": parts[2],
            "time": parts[3]
        }
        db["appointments"].append(appointment)

    elif command == "VIEW_RECORDS":
        patient_id = int(parts[1])
        records = [p for p in db["patients"] if p["id"] == patient_id]
        return json.dumps(records)

    else:
        return "ERROR: Unknown command"

    # Save database
    with open("database.json", "w") as f:
        json.dump(db, f, indent=2)

    return "OK"

def start_server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
