import os
import http.server
import socketserver
import threading
from flask import Flask, render_template, request, jsonify

# ----- HTTP Server to Receive Images -----

UPLOAD_DIR = 'static/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ImageUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        try:
            content_type = self.headers['Content-Type']
            if not content_type.startswith('image/'):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid content type')
                return

            content_length = int(self.headers['Content-Length'])
            image_data = self.rfile.read(content_length)

            # Save the image with a constant filename
            filename = os.path.join(UPLOAD_DIR, 'current_image.jpg')
            
            with open(filename, 'wb') as img_file:
                img_file.write(image_data)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Image uploaded successfully')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

server_address = ('0.0.0.0', 5000)

def run_http_server():
    with socketserver.TCPServer(server_address, ImageUploadHandler) as httpd:
        print('HTTP server listening on port 5000...')
        httpd.serve_forever()

# ----- Flask App -----

app = Flask(__name__)

# Flask configurations for production readiness
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

@app.route('/')
def display_images():
    image_names = os.listdir(UPLOAD_DIR)
    return render_template('display.html', image_names=image_names)

@app.route('/receive_notification', methods=['GET', 'POST'])
def receive_notification():
    try:
        if request.method == 'GET':
            text_data = request.args.get('data', '')
        elif request.method == 'POST':
            text_data = request.data.decode('utf-8')
        else:
            return jsonify({"error": "Unsupported request method"}), 405
        
        print("Received text data:", text_data)
        return jsonify({"message": "Notification received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Start HTTP server in a separate thread
    t1 = threading.Thread(target=run_http_server)
    t1.start()

    # Start Flask app in the main thread
    app.run(host='0.0.0.0', port=5001)

