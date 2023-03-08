import cv2
import pandas as pd

#handle mouse events
def click_event(event, x, y, flags, param):
    # Check if left button of mouse is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Initialize the position of the circle and text
        circle_pos = (x,y)
        text_pos = (x-10, y-10)
        # Check if the newly clicked point overlaps with any of the existing points
        for point in points:
            if distance(point[:2], circle_pos) < 20:
                # Offset the position of the text for the new point by a fixed amount
                text_pos = (text_pos[0], text_pos[1]-15)
        # Append the coordinates and ID of the click to the list of points
        points.append((x,y,click_id[0]))
        # Draw a circle at the clicked location
        cv2.circle(img, circle_pos, 3, (0,0,255), -1)
        # Put the ID number inside the circle
        cv2.putText(img, str(click_id[0]), text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.imshow("image", img)
        click_id[0] += 1

# Define a function to calculate the Euclidean distance between two points
def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


# Load the image using the path passed as an argument
img_path = input("Enter the path of the image file: ")
img = cv2.imread(img_path)

# Create a window to display the image
cv2.imshow("image", img)

# Create an empty list to store the clicked points
points = []

# Set the mouse callback function for the window
cv2.setMouseCallback("image", click_event)

# Initialize the ID number for the first click
click_id = [1]

# Wait for the user to close the window
cv2.waitKey(0)

# Create a pandas DataFrame from the list of points
df = pd.DataFrame(points, columns=['x', 'y', 'ID'])

# Save the DataFrame to a CSV file
csv_path = input("Enter the path where you want to save the CSV file: ")
df.to_csv(csv_path, index=False)

# Save the image with all the circles as a new image with the same filename as the original image with the suffix "circled"
circled_path = img_path[:-4] + "_circled.jpg"
cv2.imwrite(circled_path, img)

# Close all windows
cv2.destroyAllWindows()


###  green/(blue+green+red)

### Add light/weather data from the UC Davis weather stations for the final datasheet.