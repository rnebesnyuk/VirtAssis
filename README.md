# Virtassis

This is a Personal Assistant Django app developed by Django Dreams Co.

The app allows you to:
1. Save the contacts with names, addresses, phones, emails, and dates of birth to the contact book.
2. Display the list of contacts with birthdays within a certain timeframe.
3. Validate the email and phone upon input and get a notification for the user in case of an error.
4. Search the contacts by name, address, phone, and email
5. Edit and remove the contact
6. Save the notes with info
7. Search the notes by title, description and tag
8. Edit and remove the note
9. Add the tags to the notes
10. Sort the notes by tags, priority, completion
11. Upload the files to the cloud storage with access to these files. Files can be downloaded. Sort the files by categories (images, videos, docs, other) and filter them.
12. Get a short daily news overview, currencies, and weather forecasts for the upcoming days
13. Users can register in the app. In case of forgot password, it can be reset via email. Only registered users can use the functionality described above except for news, forecast, and currencies. User has access only to its own content in the app.

## Access on Web
The application is available online at
https://virtassis-3.fly.dev/

## Installation Instructions from Git
1. Clone the Repository:
   ```bash
   git clone https://github.com/rnebesnyuk/VirtAssis.git
   cd virtassis
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv venv
   ```
   ```bash
   venv\Scripts\activate
   ```
3. Install Dependencies from requirements.txt
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables:
   
   Create an .env file in the root directory of the project and configure the necessary environment variables:
   
   - `SECRET_KEY=` Django Secret Key
   - `POSTGRES_DB=` Name of the database.
   - `POSTGRES_USER=` Username for accessing the database.
   - `POSTGRES_PASSWORD=` Password for accessing the database.
   - `POSTGRES_DOMAIN=` Database domain.
   - `POSTGRES_PORT=` Port number for the database connection.
   - `MAIL_USERNAME=` Email for the mailing service host.
   - `MAIL_PASSWORD=` Password for the email host.
   - `MAIL_FROM=` Email from the specified address.
   - `MAIL_PORT=` SMTP port for email communication.
   - `MAIL_SERVER=` SMTP mailing service.
   - `CLOUDINARY_NAME=` Name of the Cloudinary domain.
   - `CLOUDINARY_API_KEY=` Cloudinary API Key.
   - `CLOUDINARY_API_SECRET=` Cloudinary API Secret.
6. App launch:
  ```bash
   python manage.py runserver
   ```
