import requests

# Set the URL of the server endpoint
url = 'http://localhost:5000/upload'

# Specify the path to your audio file
file_path = 'audio.mp3'

# Open the file in binary mode
with open(file_path, 'rb') as f:
    # Define the files in the form data with a key that the server will recognize (e.g., 'file')
    files = {'file': (file_path, f, 'audio/mpeg')}

    # Make a POST request to the server with the file
    response = requests.post(url, files=files)

    # Print the response from the server
    print(f'Server Response: {response.text}')

