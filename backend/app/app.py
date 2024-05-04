from flask import Flask, request

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Retrieve basic information about the file
    file_info = {
        'filename': file.filename,
        'content_type': file.content_type,
        'content_length': file.content_length
    }

    # Write basic information about the file to a text file
    with open('file_info.txt', 'w') as f:
        f.write(f"Filename: {file_info['filename']}\n")
        f.write(f"Content Type: {file_info['content_type']}\n")
        f.write(f"Content Length: {file_info['content_length']}\n")

    return 'File information saved successfully'


if __name__ == '__main__':
    app.run(debug=True)
