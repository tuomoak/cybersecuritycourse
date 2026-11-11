# cybersecuritycourse

## Setup

1. Clone the repository
```bash
git clone git@github.com:tuomoak/cybersecuritycourse.git
```

2. Install Django and dependencies
```bash
python3 -m pip install django "selenium<4" "urllib3<2" beautifulsoup4 requests
```

3. Apply migrations
```bash
python3 manage.py migrate
```

4. Create a superuser
```bash
python3 manage.py createsuperuser
```

## Running the app

1. Run the development server
```bash
python3 manage.py runserver
Open http://127.0.0.1:8000 in your browser
```

2. Login to admin pages
```bash
http://127.0.0.1:8000/admin
```

3. On admin pages create users and posts.

4. Login to site.
```bash
http://127.0.0.1:8000/
```