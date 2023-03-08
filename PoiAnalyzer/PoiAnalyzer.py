import pandas as pd
import os
import cv2
import numpy as np

# Define a function to find the total and average NDVI values for the object closest to a given point
def find_ndvi_value(img_path, point):
    # Load the corresponding NDVI image
    ndvi_path = img_path
    ndvi = cv2.imread(ndvi_path, cv2.IMREAD_GRAYSCALE)
    # Extract the x and y coordinates of the point
    x, y = point[:2]
    # Define the region of interest as a square with side length 50 pixels centered on the point
    roi_x1 = max(int(x - 25), 0)
    roi_y1 = max(int(y - 25), 0)
    roi_x2 = min(int(x + 25), ndvi.shape[1])
    roi_y2 = min(int(y + 25), ndvi.shape[0])
    roi = ndvi[roi_y1:roi_y2, roi_x1:roi_x2]
    # Check if the ROI is empty
    if roi.size == 0:
        return np.nan, np.nan
    # Calculate the total and average NDVI values for the ROI
    total_ndvi = roi.sum()
    average_ndvi = roi.mean()
    return total_ndvi, average_ndvi

# Define the path to the directory containing the images and NDVI images
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
        # Check if the file is an image
        if not filename.endswith("NDVI.jpg"):
            continue
        # Load the image and the corresponding NDVI image
        img_path = os.path.join(root, filename)
        ndvi_path = img_path
        if not os.path.isfile(ndvi_path):
            print(f"Error: {ndvi_path} is not a valid file path.")
            exit()
        ndvi = cv2.imread(ndvi_path, cv2.IMREAD_GRAYSCALE)
        # Loop through the points and find the NDVI values of the closest objects
        for index, row in df.iterrows():
            point = (row['x'], row['y'], row['ID'])
            total_ndvi, average_ndvi = find_ndvi_value(img_path, point)
            results.append((point[2], total_ndvi, average_ndvi, filename))

# Create a DataFrame from the list of results
results_df = pd.DataFrame(results, columns=['ID', 'Total NDVI', 'Average NDVI', 'Image Name'])

# Save the DataFrame to a CSV file
output_path = input("Enter the path of the output CSV file: ")
results_df.to_csv(output_path, index=False)
