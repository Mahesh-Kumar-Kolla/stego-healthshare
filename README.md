# Stego HealthShare

Secure Cloud-Based Medical Data Sharing Using Steganography in Medical Images

## 🔒 Project Overview

**Stego HealthShare** enables the secure sharing of sensitive medical data by embedding encrypted patient information into medical images using steganography. The images are then uploaded to an Amazon S3 cloud bucket for safe and controlled access.

This project leverages:
- **AES-based symmetric encryption** (`Fernet`)
- **LSB (Least Significant Bit) steganography**
- **AWS S3 for cloud storage**

---

## 🛠 Features

- 🔐 **Data Encryption**: Encrypt sensitive data using Fernet symmetric encryption.
- 🖼 **Image Steganography**: Embed encrypted data into PNG images using LSB manipulation.
- ☁️ **Cloud Upload**: Upload the stego-images to AWS S3 for remote access.
- 🔍 **Data Extraction**: Retrieve and decrypt hidden data from an image.

---

## 📦 Requirements

- Python 3.x
- `cryptography`
- `Pillow`
- `boto3`

Install dependencies:
```bash
pip install cryptography Pillow boto3
