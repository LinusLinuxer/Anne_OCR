# import libraries
import os
import pytesseract
from PIL import Image



# Define the function for OCR recognition and appending to a file
def ocr_images_to_text(input_folder, output_file):
    try:
        # Iterate over all files in the specified folder in reverse order
        with open(output_file, "a", encoding="utf-8") as file:
            for filename in sorted(os.listdir(input_folder), reverse=False):
                # Construct full file path
                image_path = os.path.join(input_folder, filename)

                # Open the image using PIL
                with Image.open(image_path) as img:
                    # Perform OCR on the image
                    extracted_text = pytesseract.image_to_string(img)

                    # Write the OCR result to a text file, appending the text
                    file.write(f"Text from {filename}:\n")
                    file.write(extracted_text + "\n\n")

        print(f"OCR completed. Text written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Provide the path to the folder containing images and the output text file
input_folder = "OCR_Images"
output_file = "OCR_Output/data.txt"
# Call the function
ocr_images_to_text(input_folder, output_file)
