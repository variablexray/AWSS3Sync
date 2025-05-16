# S3 Folder Sync Application

## Overview
The **S3 Folder Sync** application is a Python-based desktop tool designed to synchronize a local folder with an Amazon S3 bucket in real-time. It monitors a specified local directory for file changes (creation, modification, or deletion) and automatically reflects those changes in the designated S3 bucket. The application features a graphical user interface (GUI) built with Tkinter, making it user-friendly for configuring and managing the sync process.

## Features
- **Real-time Sync**: Automatically uploads new or modified files to S3 and deletes files from S3 when they are removed locally.
- **GUI Interface**: Allows users to configure the local folder, S3 bucket, S3 path, and AWS credentials through an intuitive interface.
- **AWS Credential Support**: Supports both explicit AWS Access Key/Secret Key entry and default AWS credentials (e.g., from AWS CLI or environment variables).
- **Configuration Persistence**: Saves configuration settings to a `config.json` file for reuse across sessions.
- **Status Monitoring**: Displays connection status and sync operations in the GUI.
- **Recursive Monitoring**: Watches all subdirectories within the specified local folder.

## Requirements
- **Python 3.x**
- **Required Python Libraries**:
  - `boto3`: For AWS S3 interactions
  - `watchdog`: For monitoring file system events
  - `tkinter`: For the GUI (usually included with Python)
- **AWS Account**: An AWS account with access to an S3 bucket.
- **AWS Credentials**: Either configured via AWS CLI/environment variables or provided manually in the GUI.

Install the required libraries using:
```bash
pip install boto3 watchdog
```

## Installation
1. Clone or download the repository containing the script.
2. Ensure Python 3.x is installed on your system.
3. Install the required dependencies (see above).
4. Run the script using:
   ```bash
   python s3_sync.py
   ```

## Usage
1. **Launch the Application**:
   - Run the script to open the GUI window.
2. **Configure Settings**:
   - **Local Folder**: Click "Browse" to select the local folder to sync.
   - **S3 Bucket**: Enter the name of the S3 bucket (e.g., `my-bucket`).
   - **S3 Path**: Specify the S3 path (prefix) within the bucket (e.g., `sync_folder/`).
   - **AWS Access Key/Secret Key** (optional): Enter your AWS credentials, or leave blank to use default credentials.
3. **Start Sync**:
   - Click "Start Sync" to begin monitoring and syncing the local folder with S3.
   - The status will update to "Connected" if successful.
4. **Stop Sync**:
   - Click "Stop Sync" to halt the monitoring process.
5. **Close the Application**:
   - Closing the window will stop any active sync and save the configuration.

## Configuration File
- A `config.json` file is automatically created in the same directory as the script to store settings (local folder, S3 bucket, S3 path, and AWS credentials).
- On startup, the application loads the previous configuration from this file, if it exists.

## Notes
- **File System Monitoring**: The application uses the `watchdog` library to monitor file system events recursively. Only file changes (not directories) trigger sync actions.
- **Error Handling**: Errors during upload or deletion are logged to the console, and connection issues are shown in a message box.
- **Security**: AWS credentials entered in the GUI are saved in plain text in `config.json`. Ensure the file is secured or use default AWS credentials for better security.
- **Limitations**: The application syncs from local to S3 only (one-way sync). Changes made directly in S3 are not reflected locally.

## Example
To sync a local folder `C:\Data` to an S3 bucket `my-bucket` under the path `backup/`, configure the GUI as follows:
- Local Folder: `C:\Data`
- S3 Bucket: `my-bucket`
- S3 Path: `backup/`
- AWS Access Key/Secret Key: (optional, if not using default credentials)

After clicking "Start Sync", any file created, modified, or deleted in `C:\Data` will be mirrored to `s3://my-bucket/backup/`.

## Troubleshooting
- **Connection Failed**: Ensure the S3 bucket exists, the AWS credentials are valid, and you have network connectivity.
- **No Sync Occurring**: Verify the local folder path is correct and that you have write permissions for the folder.
- **Missing Dependencies**: Install `boto3` and `watchdog` using pip if you encounter import errors.

## License
This project is provided as-is, with no warranty. Feel free to modify and distribute as needed.