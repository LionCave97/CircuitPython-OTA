## CircuitPython-OTA

This project provides an over-the-air (OTA) update system for CircuitPython devices using a Flask server.

### Server Setup

1. Ensure you have Python and Flask installed on your system. If not, you can install them using pip:

```bash
pip install python flask
```
2. Navigate to the project directory and start the Flask server using the following command:
```bash
flask --app server run --host=0.0.0.0
```
### Pico Setup

1. Install CircuitPython on your Raspberry Pi Pico. You can follow the instructions provided here.

2. Copy the contents of the pidata folder from the project directory to your Pico.

### Project Structure

The project consists of a Flask server (defined in server.py) that serves files from the pidata directory. The pidata directory contains the Python scripts that run on the Pico.

The Pico checks for updates by comparing the SHA256 checksums of its local files with those on the server. If any files are out of date, it downloads the updated versions from the server and replaces the local copies.

### Note

Ensure that the Pico and the server are connected to the same network and that the server's IP address and port are correctly set in the Pico's settings.toml file.
