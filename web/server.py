from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sqlite3
import json
import sys

def get_root_path(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, file_path)


class Database:
    def __init__(self, database_file_path):
        self.connection = sqlite3.connect(database_file_path)
        print('Database connection opened.')
    
    def select(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def close(self):
        self.cursor.close()
        self.connection.close()
        print('Database connection closed.')


class HumidityService:
    def __init__(self, database):
        self.database = database
    
    def get_humidity_data(self):
        rows = self.database.select('SELECT * FROM humidity')
        return [{'date': row[0], 'humidity': row[1]} for row in rows]


class AirTemperatureService:
    def __init__(self, database):
        self.database = database
    
    def get_temperature_data(self):
        rows = self.database.select('SELECT * FROM air_temperature')
        return [{'date': row[0], 'temperature': row[1]} for row in rows]


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, humidity_service, air_temperature_service, request, client_address, server):
        self.humidity_service = humidity_service
        self.air_temperature_service = air_temperature_service
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            index_path = get_root_path('index.html')
            with open(index_path, 'rb') as file:
                self.wfile.write(file.read())

        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            humidity_data = self.humidity_service.get_humidity_data()
            air_temperature_data = self.air_temperature_service.get_temperature_data()
            data = {'humidityData': humidity_data, 'airTemperatureData': air_temperature_data}
            
            self.wfile.write(json.dumps(data).encode())


        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

def run(server_class = HTTPServer, port = 8080):
    database_path = get_root_path('../db/data.db')
    database = Database(database_path)
    
    humidity_service = HumidityService(database)
    air_temperature_service = AirTemperatureService(database)
    
    server_address = ('', port)
    request_handler = lambda *args: RequestHandler(humidity_service, air_temperature_service, *args)
    httpd = server_class(server_address, request_handler)
    
    print(f"Serving at port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        database.close()

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port {}.".format(port))
    
    run(port = port)
