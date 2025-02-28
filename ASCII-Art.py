import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, simpledialog

# ASCII character sets for different contrast levels
ASCII_SETS = {
    "1": "@%#*+=-:. ",  # High contrast (simple)
    "2": "@&%B8WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`\'. ",  # Medium contrast (detailed)
    "3": "@#*+=:. "  # Low contrast (minimalist)
}

def open_file_dialog(file_types):
    """Open file explorer to select a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=file_types)
    return file_path

def choose_ascii_set():
    """Prompt user to select ASCII contrast level."""
    print("\nChoose ASCII contrast level:")
    print("1 - High contrast")
    print("2 - Medium contrast")
    print("3 - Low contrast")
    
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in ASCII_SETS:
            return ASCII_SETS[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")

def image_to_ascii(image_path, ascii_chars, output_width=150):
    """Convert an image to ASCII and display it in a window."""
    try:
        img = Image.open(image_path).convert("L")  # Convert to grayscale
        width, height = img.size
        aspect_ratio = height / width
        new_height = int(output_width * aspect_ratio * 0.55)
        img = img.resize((output_width, new_height))

        pixels = np.array(img)
        ascii_image = [[ascii_chars[pixel * len(ascii_chars) // 256] for pixel in row] for row in pixels]

        display_ascii(ascii_image)
    except Exception as e:
        print(f"Error: {e}")

def video_to_ascii(video_path, ascii_chars, output_width=150):
    """Convert a video to ASCII and display it frame by frame."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = process_frame_to_ascii(frame, ascii_chars, output_width)
        display_ascii(ascii_frame)

        if cv2.getWindowProperty("ASCII Art", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

def webcam_to_ascii(ascii_chars, output_width=150):
    """Convert live webcam video to ASCII in real-time."""
    cap = cv2.VideoCapture(0)  # Open default webcam

    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = process_frame_to_ascii(frame, ascii_chars, output_width)
        display_ascii(ascii_frame)

        if cv2.getWindowProperty("ASCII Art", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

def process_frame_to_ascii(frame, ascii_chars, output_width):
    """Convert a frame to ASCII format."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray_frame.shape
    aspect_ratio = height / width
    new_height = int(output_width * aspect_ratio * 0.55)
    resized_frame = cv2.resize(gray_frame, (output_width, new_height))

    ascii_frame = [[ascii_chars[pixel * len(ascii_chars) // 256] for pixel in row] for row in resized_frame]
    return ascii_frame

def display_ascii(ascii_matrix, font_size=10):
    """Render ASCII art in an OpenCV window."""
    height, width = len(ascii_matrix), len(ascii_matrix[0])
    img = np.ones((height * font_size, width * font_size, 3), dtype=np.uint8) * 0

    for i, row in enumerate(ascii_matrix):
        for j, char in enumerate(row):
            cv2.putText(img, char, (j * font_size, i * font_size),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

    cv2.imshow("ASCII Art", img)
    cv2.waitKey(1)

# Main function for user input
if __name__ == "__main__":
    choice = input("Enter 'i' for image, 'v' for video, 'w' for webcam ->  ").strip().lower()
    
    ascii_chars = choose_ascii_set()  # Let user select ASCII contrast

    if choice == "i":
        image_path = open_file_dialog([("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if image_path:
            image_to_ascii(image_path, ascii_chars)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("No file selected.")
    elif choice == "v":
        video_path = open_file_dialog([("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        if video_path:
            video_to_ascii(video_path, ascii_chars)
        else:
            print("No file selected.")
    elif choice == "w":
        print("Starting webcam ASCII... ")
        webcam_to_ascii(ascii_chars)
    else:
        print("Invalid choice.")
