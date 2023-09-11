import board
import microcontroller
import os
import ssl
import wifi
import socketpool
import adafruit_requests
import adafruit_hashlib as hashlib
import json

update = True
base_url = os.getenv('base_url')

def download_file(url):
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            response.close()
            return content
        else:
            print("Failed to download file from the server. HTTP status code:", response.status_code)
            return None
    except Exception as e:
        print("Error while downloading file:", str(e))
        return None

def calculate_sha256(content):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(content)
    return sha256_hash.hexdigest()

def check_files():
    file_list_url = base_url + "/file_list"
    out_of_date_files = []
    try:
        response = download_file(file_list_url)
        if response:
            server_files = json.loads(response)
            for server_file in server_files:
                filename, server_sha256, server_timestamp = server_file
                try:
                    with open("/" + filename.replace("\\", "/"), "r") as local_file:
                        local_content = local_file.read()
                        local_sha256 = calculate_sha256(local_content.encode())
                except OSError:
                    print(f"Local file {filename} not found.")
                    local_sha256 = None

                if local_sha256 != server_sha256:
                    print(f"Newer version of {filename} found.")
                    out_of_date_files.append(filename)
                else:
                    print(f"{filename} is up to date.")
    except Exception as e:
        print("Error while checking files:", str(e))
    return out_of_date_files

def update_files(out_of_date_files):
    for filename in out_of_date_files:
        file_content = download_file(base_url + "/download/" + filename)
        if file_content:
            update_file(filename, file_content)
        else:
            print(f"Failed to download {filename} from the server.")

def update_file(filename, content):
    try:
        with open("/test.txt", "w") as file:
            pass
        os.remove("/test.txt")
    except OSError:
        print("The filesystem is read-only.")
        return
    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"File {filename} updated successfully.")
    except OSError as e:
        print(f"Failed to update file {filename}: {str(e)}")


def AutoUpdate():
    for i in range(3):
        try:
            print("Connecting to WiFi")
            wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
            print("Connected to WiFi")
            print("Updating! Pulling files")
            update_list = check_files()
            
            if len(update_list) > 0:
                print("We need to update", len(update_list), "Files")
                print("Updating files now! Then rebooting")  
                update_files(update_list)
                microcontroller.reset()
            else:
                print("No update needed!")
            break  # If the above code is successful, break the loop
        except Exception as e:
            print(f"Attempt {i+1} failed. Retrying...")
            print("Error:\n", str(e))
            if i == 2:  # If this was the third attempt, abort
                print("Failed to connect after 3 attempts. Aborting.")