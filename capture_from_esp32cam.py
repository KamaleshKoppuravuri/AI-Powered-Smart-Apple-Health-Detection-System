import os
import requests

esp32_cam_url = "http://192.168.196.97/capture"
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)

def capture_image(counter):
    response = requests.get(esp32_cam_url)
    if response.status_code == 200:
        file_path = os.path.join(save_dir, f"test_image_{counter}.jpg")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f" Image saved: {file_path}")
    else:
        print("Failed to capture image")

def main():
    counter = 1
    print("📸 Press 'c' to capture image or 'q' to quit.")
    while True:
        key = input("Press key: ").strip().lower()
        if key == 'c':
            capture_image(counter)
            counter += 1
        elif key == 'q':
            print(" Exiting...")
            break
        else:
            print("Press 'c' to capture or 'q' to quit.")

if __name__ == "__main__":
    main()
