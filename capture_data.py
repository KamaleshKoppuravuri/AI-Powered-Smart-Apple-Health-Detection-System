import cv2

def find_external_camera():
    print("Scanning for available cameras...")
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera found at index {i}")
                cap.release()
                return i
            cap.release()
        print(f"No camera at index {i}")
    return Noneq

# Step 1: Automatically find the external webcam index
external_cam_index = find_external_camera()

if external_cam_index is None:
    print(" No webcam found. Please connect an external webcam.")
    exit()

# Step 2: Open the external webcam
cap = cv2.VideoCapture(external_cam_index)
if not cap.isOpened():
    print(f" Failed to open webcam at index {external_cam_index}")
    exit()

print("External webcam is live. Press 'c' to capture and overwrite 'test_image.jpg', 'q' to quit.")

# Step 3: Loop for displaying and capturing
while True:
    ret, frame = cap.read()
    if not ret:
        print(" Couldn't read frame.")
        break

    cv2.imshow("External Webcam", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        filename = "test_image.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image overwritten as {filename}")
    elif key == ord('q'):
        print("Exiting...")
        break

# Step 4: Release resources
cap.release()
cv2.destroyAllWindows()
