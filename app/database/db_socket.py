import socket
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fletface'
}

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 80))  
    server_socket.listen()

    print("Server is listening for connections...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(conn)

def handle_client(conn):
    try:
        user_id = conn.recv(1024).decode('utf-8')
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()
        query = "DELETE FROM employees WHERE id = %s"
        cursor.execute(query, (user_id,))
        db_connection.commit()

        if cursor.rowcount > 0:
            conn.sendall("User deleted successfully.".encode('utf-8'))
        else:
            conn.sendall("User not found.".encode('utf-8'))

    except mysql.connector.Error as err:
        conn.sendall(f"Database error: {err}".encode('utf-8'))
    finally:
        cursor.close()
        db_connection.close()
        conn.close()

if __name__ == '__main__':
    start_socket_server()
