# File Encryption/Decryption App

This Flask application provides a user-friendly interface for encrypting and decrypting files using two popular encryption algorithms: **Fernet** and **AES**. It allows users to securely encrypt files and retrieve them along with the generated encryption key. The application also supports decryption of files by using the corresponding key.

## Features

- **Encryption Algorithms**: Supports both Fernet and AES encryption.
- **File Uploads**: Users can upload files for encryption and decryption.
- **Key Management**: Generates and saves encryption keys for AES and Fernet, ensuring secure key management.
- **User Interface**: A simple and intuitive web interface for performing encryption and decryption operations.
- **Error Handling**: Robust error handling for file upload and encryption/decryption processes.

## Technologies Used

- **Flask**: A micro web framework for Python to handle HTTP requests and responses.
- **Cryptography**: A Python library that provides cryptographic recipes and primitives.
- **HTML/CSS**: For creating a responsive and user-friendly interface.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/repository-name.git
   cd repository-name
# Update package list
sudo apt update

# Install Python and pip if not already installed
sudo apt install python3 python3-pip -y

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Activate the virtual environment

# Install Flask and cryptography
pip install Flask cryptography

# To exit the virtual environment later, use:
deactivate
