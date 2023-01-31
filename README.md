PDF Metadata Management Web App
This is a Flask web app for managing the metadata of PDF files. The app allows you to upload a PDF file, extract its metadata, and save it to a database. It also provides features for searching, displaying and listing the metadata in the database.

Features
Upload PDF files
Extract metadata from the PDF files
Save the metadata to a database (SQLite)
Display the metadata in a table
Search metadata by ID
Requirements
Flask
pikepdf
sqlite3
How to run the app
Clone the repository
Install the required packages by running pip install -r requirements.txt
Start the server by running python app.py
Access the app in your browser at http://localhost:5000/
File Structure
app.py contains the main code for the web app
templates/ contains the HTML templates for the app
static/ contains the CSS files for styling the app
Usage
Open the app in your browser at http://localhost:5000/.
Click on the "Upload Metadata" button, select a PDF file and click "Submit".
The metadata of the PDF file will be displayed on the screen.
Click on "Save to Database" to save the metadata to the SQLite database.
Click on "List Metadata" to view the metadata stored in the database.
To search for a specific metadata, click on "Search Metadata" and enter the ID.
Note
The app uses an SQLite database named metadata.db to store the metadata information.
The columns in the database table are dynamically created based on the metadata fields of the uploaded PDF files.