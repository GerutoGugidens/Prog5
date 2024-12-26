import http.server
import socketserver

PORT = 8000


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


# Запуск сервера
with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Сервер запущен на порту {PORT}. Раздаёт модули из текущей директории.")
    httpd.serve_forever()
