import pandas as pd
import os
import cv2
import numpy as np

# Define a function to find the green/(red+blue+green) ratio for the object closest to a given point
def find_green_ratio(img_path, point):
    # Load the image
    img = cv2.imread(img_path)
    # Check if the image is empty
    if img is None:
        print(f"Error: Unable to read the image at {img_path}.")
        return np.nan
    
    # Convert the image from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Extract the x and y coordinates of the point
    x, y = point[:2]
    # Define the region of interest as a square with side length 50 pixels centered on the point
    roi_x1 = max(int(x - 25), 0)
    roi_y1 = max(int(y - 25), 0)
    roi_x2 = min(int(x + 25), img.shape[1])
    roi_y2 = min(int(y + 25), img.shape[0])
    roi = img[roi_y1:roi_y2, roi_x1:roi_x2]
    # Check if the ROI is empty
    if roi.size == 0:
        return np.nan
    # Calculate the green/(red+blue+green) ratio for the ROI
    green = roi[:, :, 1].sum()
    total_rgb = roi.sum()
    green_ratio = green / total_rgb
    return green_ratio

# Define the path to the directory containing the images
folder_path = input("Enter the path of the folder containing the images: ")
if not os.path.isdir(folder_path):
    print(f"Error: {folder_path} is not a valid folder path.")
    exit()

# Load the list of points from the CSV file
points_path = input("Enter the path of the CSV file containing the list of points: ")
if not os.path.isfile(points_path):
    print(f"Error: {points_path} is not a valid file path.")
    exit()
df = pd.read_csv(points_path)

# Initialize the list of results
results = []

# Loop through the files in the folder and its subdirectories
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        # Check if the file is an image and not an NDVI image
        if not filename.endswith(".jpg") or filename.endswith("NDVI.jpg"):
            continue
        # Load the image
        img_path = os.path.join(root, filename)
        # Loop through the points and find the green/(red+blue+green) ratio of the closest objects
        for index, row in df.iterrows():
            point = (row['x'], row['y'], row['ID'])
            green_ratio = find_green_ratio(img_path, point)
            results.append((point[2], green_ratio, filename))

# Create a DataFrame from the list of results
results_df = pd.DataFrame(results, columns=['ID', 'Green Ratio', 'Image Name'])

# Save the DataFrame to a CSV file
output_path = input("Enter the path of the output CSV file: ")
results_df.to_csv(output_path, index=False)
