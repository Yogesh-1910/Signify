import os
import cv2
import numpy as np
import sys

def generate_handwriting_video(input_text, samples, output_file="output.mp4"):
    """
    Generate handwriting-like text on a white A4 sheet as an animated video.

    Args:
        input_text (str): Text to replicate.
        samples (dict): Dictionary of character PNG images.
        output_file (str): Output video file name.
    """
    # A4 size in pixels at 300 DPI (approximately)
    A4_WIDTH, A4_HEIGHT = 2480, 3508
    IMG_HEIGHT = 1000  # Fixed height for each character
    LETTER_SPACING = -20  # Reduced space between characters (negative values allow slight overlaps)
    SPACE_WIDTH = IMG_HEIGHT // 1  # Width for spaces between words
    LINE_SPACING = 50  # Space between lines

    # Create a white A4-sized background
    a4_image = np.ones((A4_HEIGHT, A4_WIDTH, 3), dtype=np.uint8) * 255

    x_offset = 50  # Starting x-coordinate for placing characters (left margin)
    y_offset = 50  # Starting y-coordinate for placing the first line (top margin)

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use H.264 codec for MP4
    fps = 5  # Frames per second
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (A4_WIDTH, A4_HEIGHT))

    for char in input_text:
        if char == " ":
            # Add space between words
            x_offset += SPACE_WIDTH
            continue

        # Get the character image from samples
        char_image = samples.get(char.lower())
        if char_image is None:
            print(f"Character '{char}' not found in samples.")
            continue

        # Resize the character image to fit the fixed height while maintaining aspect ratio
        char_h, char_w, _ = char_image.shape
        scale = IMG_HEIGHT / char_h
        new_w = int(char_w * scale)
        char_image_resized = cv2.resize(char_image, (new_w, IMG_HEIGHT), interpolation=cv2.INTER_AREA)

        # Check if the character will exceed the line width
        if x_offset + char_image_resized.shape[1] > A4_WIDTH - 50:  # Account for the right margin
            # Move to the next line
            x_offset = 50  # Reset x-coordinate
            y_offset += IMG_HEIGHT + LINE_SPACING

            # Check if there's space for a new line
            if y_offset + IMG_HEIGHT > A4_HEIGHT - 50:  # Account for the bottom margin
                print("Reached the end of the A4 page.")
                break

        # Handle transparent PNGs: Blend with the white background
        if char_image_resized.shape[2] == 4:  # If the image has an alpha channel
            alpha_channel = char_image_resized[:, :, 3] / 255.0  # Normalize alpha to 0-1
            for c in range(3):  # Iterate over R, G, B channels
                a4_image[y_offset:y_offset + IMG_HEIGHT, x_offset:x_offset + new_w, c] = (
                    char_image_resized[:, :, c] * alpha_channel +
                    a4_image[y_offset:y_offset + IMG_HEIGHT, x_offset:x_offset + new_w, c] * (1 - alpha_channel)
                )
        else:
            # Directly overlay if no alpha channel
            a4_image[y_offset:y_offset + IMG_HEIGHT, x_offset:x_offset + new_w] = char_image_resized

        # Write the current frame to the video
        video_writer.write(a4_image)

        x_offset += new_w + LETTER_SPACING  # Update the x_offset for the next character

    # Release the video writer
    video_writer.release()
    print(f"Generated handwriting video saved to {output_file}")


# Load the samples as a dictionary
sign_samples_dir = "webpage/sign_samples"
samples = {}
for filename in os.listdir(sign_samples_dir):
    if filename.endswith(".png"):
        char = filename.split(".")[0].lower()
        img = cv2.imread(os.path.join(sign_samples_dir, filename), cv2.IMREAD_UNCHANGED)
        samples[char] = img

# Use command-line arguments for input text
if len(sys.argv) > 1:
    user_input = sys.argv[1]
else:
    user_input = input("Enter the text to replicate: ")

generate_handwriting_video(user_input, samples, output_file="output.mp4")