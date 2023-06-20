# Virtassis

This is a Personal Assistant Django app developed by Django Dreams Co.

The app allows you to:
1. Save the contacts with names, addresses, phones, emails, and dates of birth to the contact book.
2. Display the list of contacts with birthdays within a certain timeframe.
3. Validate the email and phone upon input and get a notification for the user in case of an error.
4. Search the contacts by name, address, phone, and email
5. Edit and remove the contact
6. Save the notes with info
7. Search the notes by title, descriptionб and tag
8. Edit and remove the note
9. Add the tags to the notes
10. Sort the notes by tags, priority, completion
11. Upload the files to the cloud storage with access to these files. Files can be downloaded. Sort the files by categories (images, videos, docs, other) and filter them.
12. Get a short daily news overview, currencies, and weather forecasts for the upcoming days
13. Users can register in the app. In case of forgot password, it can be reset via email. Only registered users can use the functionality described above except for news, forecast, and currencies. User has access only to its own content in the app.

You need the .env file with environment variables to work with the app. Please create the file with the following variables and insert your values:

# Django Secret Key

SECRET_KEY=

# Database PostgreSQL
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DOMAIN=
POSTGRES_PORT=

# Email service
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

# Cloudinary Storage
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# App launch:

python manage.py runserver
