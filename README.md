# TiffinHub

TiffinHub is a Django-based web application that provides tiffin services to users through vendors. Users can register as either customers or vendors. Vendors can update their daily menus and offer their services, which customers can subscribe to or buy. The application also tracks subscriptions and unsubscriptions.

## Features

- User authentication and registration (customers and vendors)
- Vendor profile management
- Customer subscription management
- Track past and current subscriptions
  
## Technologies Used

### Backend
- Python 3.6+
- Django 3.0+
- Pillow (for handling image uploads)
- MySQL (as the database)

### Frontend
- HTML
- CSS
- JavaScript

## Installation
To get up and running, simply do the following and set your admin username and password when prompted.
```
git clone https://github.com/MonikaChoudhary752/TiffinHub.git
cd TiffinHub
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```
