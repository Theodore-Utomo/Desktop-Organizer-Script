import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

folders = {
    "Images": [".png", ".jpeg", ".jpg", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Music": [".mp3", ".wav", ".aac"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Others": []
}

for folder in folders:
    folder_path = os.path.join(desktop_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(desktop_path):
            src = os.path.join(desktop_path, filename)
            if os.path.isfile(src):
                file_ext = os.path.splitext(filename)[1].lower()
                moved = False
                for folder, extensions in folders.items():
                    if file_ext in extensions:
                        dest_folder = os.path.join(desktop_path, folder)
                        shutil.move(src, os.path.join(dest_folder, filename))
                        moved = True
                        break
                if not moved:
                    dest_folder = os.path.join(desktop_path, "Others")
                    shutil.move(src, os.path.join(dest_folder, filename))

observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, desktop_path, recursive=False)

observer.start()

try:
    while True:
        time.sleep(10) 
except KeyboardInterrupt:
    observer.stop()
observer.join()

