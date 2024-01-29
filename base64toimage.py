import os
import mysql.connector
import base64
from io import BytesIO
from PIL import Image



# Connect to your MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Lutasie6928",
    database="irisimg"
)
cursor = db_connection.cursor()

# Fetch data from the table
cursor.execute("SELECT irisImgId, irisHashed, irisId FROM irisimg") #irisimg is the table name
rows = cursor.fetchall()

# Root folder to save the decoded images
output_root_folder = r"C:\Users\ACER\Downloads\HANNIE\master\DATA\irisimageoutput"

# Iterate through the rows and decode/save images
for row in rows:
    irisImgId, irisHashed_base64, irisId = row
    try:
        # Check if the data is a base64 string
        if irisHashed_base64.startswith("data:image/bmp;base64,"):
            # Remove the "data:image/Png;base64," prefix
            irisHashed_base64 = irisHashed_base64[len("data:image/Png;base64,"):]

            # Decode base64 string to bytes
            img_data = base64.b64decode(irisHashed_base64)

            # Create a folder for each irisId if it doesn't exist
            output_folder = os.path.join(output_root_folder, str(irisId))
            os.makedirs(output_folder, exist_ok=True)

            # Open the image using PIL
            img = Image.open(BytesIO(img_data))

            # Save the image to the output folder
            img.save(os.path.join(output_folder, f"iris_{irisImgId}.png"))

            print(f"Image {irisImgId} saved successfully in folder {irisId}.")
        else:
            # If it's not a base64 string, print a message and handle accordingly
            print(f"Skipping image {irisImgId}: Not a base64 string")
    except Exception as e:
        print(f"Error processing image {irisImgId}: {str(e)}")

# Close the database connection
cursor.close()
db_connection.close()