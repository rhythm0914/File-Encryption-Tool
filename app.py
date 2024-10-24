from flask import Flask, request, jsonify, render_template
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)

# Define the directory to save files
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_aes_key():
    return os.urandom(16)  # AES-128

def aes_encrypt(data, key):
    iv = os.urandom(16)  # AES block size
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = iv + encryptor.update(data) + encryptor.finalize()  # Prepend IV
    return encrypted_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected for encryption.'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for encryption.'}), 400
    
    algorithm = request.form.get('algorithm', 'fernet')  # Default to Fernet
    file_data = file.read()

    if algorithm == 'fernet':
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
    elif algorithm == 'aes':
        key = generate_aes_key()
        encrypted_data = aes_encrypt(file_data, key)
    else:
        return jsonify({'error': 'Unsupported encryption algorithm.'}), 400

    # Save the encrypted file
    encrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'encrypted_{file.filename}')
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(encrypted_data)

    # Save the encryption key
    key_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encryption_key.key')
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)

    return jsonify({
        'message': 'Encryption completed successfully.',
        'encrypted_file': encrypted_file_path,
        'key_file': key_file_path
    })

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files or 'key' not in request.files:
        return jsonify({'error': 'No file or key selected for decryption.'}), 400
    
    file = request.files['file']
    key_file = request.files['key']

    if file.filename == '' or key_file.filename == '':
        return jsonify({'error': 'No file or key selected for decryption.'}), 400

    # Read the encrypted file data and key data
    encrypted_data = file.read()
    key = key_file.read()

    algorithm = request.form.get('algorithm', 'fernet')  # Get the selected algorithm

    try:
        if algorithm == 'fernet':
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
        elif algorithm == 'aes':
            iv = encrypted_data[:16]  # Extract IV
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()  # Decrypt data
        else:
            return jsonify({'error': 'Unsupported encryption algorithm.'}), 400

        # Save the decrypted file
        decrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'decrypted_{file.filename}')
        with open(decrypted_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        return jsonify({
            'message': 'Decryption completed successfully.',
            'decrypted_file': decrypted_file_path
        })
    
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
