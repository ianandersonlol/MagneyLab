

import pandas as pd
import os
# Load the input CSV file
input_path = input("Enter the path of the input CSV file: ")
if not os.path.isfile(input_path):
    print(f"Error: {input_path} is not a valid file path.")
    exit()
df = pd.read_csv(input_path)

# Extract the date and time information from the 'Image Name' column
date_list = []
time_list = []
for name in df['Image Name']:
    datetime_str = name.split("_")[1:7]
    date_str = "-".join(datetime_str[:3])
    time_str = ":".join(datetime_str[3:])
    date_list.append(date_str)
    time_list.append(time_str)

# Add the date and time columns to the DataFrame
df['Date'] = date_list
df['Time'] = time_list

# Save the updated DataFrame to a new CSV file
output_path = input("Enter the path of the output CSV file: ")
df.to_csv(output_path, index=False)