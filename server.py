from flask import Flask, send_file, request, jsonify
import datetime
import hashlib
import os

app = Flask(__name__)

# File URL for main.py on the server
main_py_url = "./pidata/"

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as firmware_file:
        for chunk in iter(lambda: firmware_file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

@app.route('/download/<filename>', methods=['GET'])
def serve_file(filename):
    file_path = os.path.join(main_py_url, filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    md5_checksum = calculate_sha256(file_path)

    response = send_file(file_path, as_attachment=True)
    response.headers['X-MD5-Checksum'] = md5_checksum

    return response

@app.route('/file_list', methods=['GET'])
def serve_file_list():
    local_folder = "./pidata"
    file_list = get_files_with_sha256(local_folder)
    return jsonify(file_list)

def get_files_with_sha256(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            filepath = os.path.join(root, filename)
            sha256_checksum = calculate_sha256(filepath)
            # Get the last modification time and convert it to a datetime object
            last_update = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            # Format the datetime object as a string
            last_update_str = last_update.strftime('%Y-%m-%d %H:%M:%S')
            # Remove the initial part of the path (local_folder) to get the relative path
            relative_path = os.path.relpath(filepath, folder)
            # Replace backslashes with forward slashes
            relative_path = relative_path.replace('\\', '/')
            file_list.append((relative_path, sha256_checksum, last_update_str))
    return file_list



@app.route('/sync_files', methods=['POST'])
def sync_files():
    # Get the file data and filename from the request
    file_data = request.data
    filename = request.headers.get('X-Filename')

    if not filename:
        return "Filename missing in request headers", 400

    filename = os.path.basename(filename)

    # Calculate MD5 checksum of the received file data
    received_md5_checksum = hashlib.md5(file_data).hexdigest()

    # Save the received file to the server folder
    try:
        with open('./pidata' + filename, 'wb') as file:
            file.write(file_data)
    except Exception as e:
        return "Error saving file on the server: " + str(e), 500

    # Respond with the received MD5 checksum for verification
    return received_md5_checksum, 200

if __name__ == '__main__':
    # Replace '0.0.0.0' and '5000' with the appropriate host and port for your deployment
    app.run(host='0.0.0.0', port=5000)
