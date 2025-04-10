import base64
import json
import os
from cryptography.fernet import Fernet
from PIL import Image
import boto3

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_bytes = f.encrypt(data.encode())
    return base64.b64encode(encrypted_bytes).decode()

def decrypt_data(encrypted_b64, key):
    f = Fernet(key)
    encrypted_bytes = base64.b64decode(encrypted_b64)
    return f.decrypt(encrypted_bytes).decode()

def embed_data_into_image(image_path, encrypted_data, output_path):
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())
    binary_data = ''.join(format(b, '08b') for b in encrypted_data.encode())
    binary_data += '11111110'  # 8-bit end marker
    
    new_pixels = []
    data_index = 0
    
    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(len(new_pixel)):
            if data_index < len(binary_data):
                new_pixel[i] = new_pixel[i] & ~1 | int(binary_data[data_index])
                data_index += 1
        new_pixels.append(tuple(new_pixel))
    
    img.putdata(new_pixels)
    img.save(output_path)

def extract_data_from_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_data = "".join(str(value & 1) for pixel in pixels for value in pixel)

    bytes_list = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    extracted_bytes = []
    for byte in bytes_list:
        if byte == '11111110': 
            break
        extracted_bytes.append(byte)

    extracted_binary = "".join(chr(int(b, 2)) for b in extracted_bytes)
    return extracted_binary


def upload_to_s3(file_path, bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
        print(f"File {file_path} successfully uploaded to {bucket_name}.")
    except Exception as e:
        print(f"Failed to upload file: {e}")

def main():
    key = generate_key()
    print("Generated Key:", key.decode())
    
    data = input("Enter the data to encrypt: ")
    encrypted_data = encrypt_data(data, key)
    print("Encrypted Data (Base64 Encoded):", encrypted_data)
    
    image_path = "input_image.png"
    output_path = "output_image.png"
    embed_data_into_image(image_path, encrypted_data, output_path)
    print("Data embedded into image.")
    
    extracted_encrypted_data = extract_data_from_image(output_path)
    print("Extracted Encrypted Data (Base64 Encoded):", extracted_encrypted_data)
    
    decrypted_data = decrypt_data(extracted_encrypted_data, key)
    print("Decrypted Data:", decrypted_data)
    
    bucket_name = "your-s3-bucket"
    upload_to_s3(output_path, bucket_name)

if __name__ == "__main__":
    main()

