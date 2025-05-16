import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import boto3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration file path/filename
# This will automatically get created if one is not found.
# Otherwise, it"ll read what has been previously configured
CONFIG_FILE = "config.json"

class S3SyncHandler(FileSystemEventHandler):
    def __init__(self, local_folder, bucket_name, s3_path, s3_client):
        self.local_folder = local_folder
        self.bucket_name = bucket_name
        self.s3_path = s3_path
        self.s3_client = s3_client

    def on_modified(self, event):
        if not event.is_directory:
            self.upload_to_s3(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.upload_to_s3(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.delete_from_s3(event.src_path)

    def upload_to_s3(self, file_path):
        relative_path = os.path.relpath(file_path, self.local_folder)
        s3_key = os.path.join(self.s3_path, relative_path).replace("\\", "/")
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            print(f"Uploaded: {file_path} -> s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error uploading {file_path}: {e}")

    def delete_from_s3(self, file_path):
        relative_path = os.path.relpath(file_path, self.local_folder)
        s3_key = os.path.join(self.s3_path, relative_path).replace("\\", "/")
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            print(f"Deleted from S3: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

class S3SyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S3 Folder Sync")
        
        self.local_folder = tk.StringVar()
        self.s3_bucket = tk.StringVar()
        self.s3_path = tk.StringVar()
        self.aws_access_key = tk.StringVar()
        self.aws_secret_key = tk.StringVar()
        self.status = tk.StringVar(value="Disconnected")
        self.recent_operation = tk.StringVar()
        self.syncing = False
        
        self.load_config()
        
        tk.Label(root, text="Local Folder").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.local_folder, width=40).grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse_folder).grid(row=0, column=2)
        
        tk.Label(root, text="S3 Bucket").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.s3_bucket, width=40).grid(row=1, column=1)
        
        tk.Label(root, text="S3 Path").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.s3_path, width=40).grid(row=2, column=1)
        
        tk.Label(root, text="AWS Access Key (Optional)").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.aws_access_key, width=40, show="*").grid(row=3, column=1)
        
        tk.Label(root, text="AWS Secret Key (Optional)").grid(row=4, column=0)
        tk.Entry(root, textvariable=self.aws_secret_key, width=40, show="*").grid(row=4, column=1)
        
        self.sync_button = tk.Button(root, text="Start Sync", command=self.toggle_sync)
        self.sync_button.grid(row=5, column=0, columnspan=3)
        
        tk.Label(root, text="Status:").grid(row=6, column=0)
        tk.Label(root, textvariable=self.status).grid(row=6, column=1)

        tk.Label(root, textvariable=self.recent_operation).grid(row=1, column=1)
        
        self.s3_client = None
        self.observer = None
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.local_folder.set(folder)
    
    def toggle_sync(self):
        if self.syncing:
            self.stop_sync()
        else:
            self.start_sync()
    
    def start_sync(self):
        try:
            aws_access_key = self.aws_access_key.get().strip() or None
            aws_secret_key = self.aws_secret_key.get().strip() or None
            
            if aws_access_key and aws_secret_key:
                self.s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                self.s3_client = boto3.client("s3")  # Use default AWS credentials
            
            self.status.set("Connected")
            self.sync_button.config(text="Stop Sync")
            self.syncing = True
            
            self.save_config()
            
            event_handler = S3SyncHandler(self.local_folder.get(), self.s3_bucket.get(), self.s3_path.get(), self.s3_client)
            self.observer = Observer()
            self.observer.schedule(event_handler, self.local_folder.get(), recursive=True)
            self.observer.start()
            
            messagebox.showinfo("Success", "Sync Started Successfully")
        except Exception as e:
            self.status.set("Connection Failed")
            messagebox.showerror("Error", str(e))
    
    def stop_sync(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        self.status.set("Disconnected")
        self.sync_button.config(text="Start Sync")
        self.syncing = False
    
    def save_config(self):
        config = {
            "local_folder": self.local_folder.get(),
            "s3_bucket": self.s3_bucket.get(),
            "s3_path": self.s3_path.get(),
            "aws_access_key": self.aws_access_key.get(),
            "aws_secret_key": self.aws_secret_key.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.local_folder.set(config.get("local_folder", ""))
                self.s3_bucket.set(config.get("s3_bucket", ""))
                self.s3_path.set(config.get("s3_path", ""))
                self.aws_access_key.set(config.get("aws_access_key", ""))
                self.aws_secret_key.set(config.get("aws_secret_key", ""))
    
    def on_closing(self):
        self.stop_sync()
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = S3SyncApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
