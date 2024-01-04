import os
import time
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f'New file {event.src_path} has been added.')

            # Resize the image
            try:
                with Image.open(event.src_path) as img:
                    # Calculate 20% of original dimensions
                    width, height = img.size
                    new_width = int(width * 0.2)
                    new_height = int(height * 0.2)

                    # Resize while maintaining aspect ratio
                    img.thumbnail((new_width, new_height))

                    # Save the resized image with "_resized" suffix
                    base_name, extension = os.path.splitext(event.src_path)
                    resized_file_path = f"{base_name}_resized{extension}"
                    img.save(resized_file_path)
                    print(f'Resized image saved to {resized_file_path}')
            except Exception as e:
                print(f'Error resizing image: {e}')

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, "C:\\Users\\Nick\\Downloads", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
