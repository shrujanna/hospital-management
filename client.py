import socket

HOST = 'localhost'
PORT = 12345

def send_request(request):
    with socket.socket() as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        return s.recv(1024).decode()

def main():
    while True:
        print("\n--- Hospital Management System ---")
        print("1. Login")
        print("2. Register Patient")
        print("3. Book Appointment")
        print("4. View Patient Records")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            u = input("Username: ")
            p = input("Password: ")
            print(send_request(f"LOGIN|{u}|{p}"))

        elif choice == '2':
            name = input("Name: ")
            age = input("Age: ")
            gender = input("Gender: ")
            print(send_request(f"REGISTER_PATIENT|{name}|{age}|{gender}"))

        elif choice == '3':
            pid = input("Patient ID: ")
            doc = input("Doctor Name: ")
            time = input("Time: ")
            print(send_request(f"BOOK_APPOINTMENT|{pid}|{doc}|{time}"))

        elif choice == '4':
            pid = input("Patient ID: ")
            print("Patient Records:", send_request(f"VIEW_RECORDS|{pid}"))

        elif choice == '5':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
