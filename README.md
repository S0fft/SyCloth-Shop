# SyCloth
Clothing shop — SSR ecommerce project on Django + API on DRF

SyCloth - it's not big clothing shop, wich give standars possiblities for clients.
In the project created 4 applications: products, users, orders, api.

Stack:
 - Pyhton
 - Django
 - PostgreSQL
 - Redis
 - Celery

Also, the following libraries were used: python-decouple, Pillow, django-allauth, django-debug-toolbar and others.

## Local deployment

### Stack Install and Creating The Root Directory
To begin, install: [Python](https://www.python.org/downloads/) | [PostgreSQL](https://www.postgresql.org/) | [Redis](https://redis.io/)
<br>
Now, create a root folder on your computer. Next, open it in a code editor or IDE.

### Venv
Create virtual environment:
```powershell
python -m venv .venv
```

And activate it:

```powershell
.venv\Scripts\Activate
``` 
### Packages
Next, install packages:

```powershell
pip install --upgrade pip
``` 
```powershell
pip install -r requirements.txt
```

 ### Fixtures and Migrations
Apply migration and load data from fixture for products and appearance other information:

```powershell
python manage.py migrate
```

```powershell
python manage.py loaddata <path_to_fixture_files>
```

### Redis and Celery
After, launch Redis and Celery using these commands:

```powershell
redis-server
```

```powershell
celery -A store worker --loglevel=INFO
```
### Server Rise
Then, run server:

```powershell
python manage.py runserver
```

