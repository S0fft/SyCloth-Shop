# SyCloth
#### Clothing-Shop — SSR ecommerce project on Django + API on Django REST Framework

The online clothing store with registration/authorization, a
shopping cart, user-profile-settings, a configured admin
panel and order payment functionality (Stripe). Implemented
email-verification. Created API. Unit Tests are written. OAuth
2.0 added. For storage using PostgreSQL.

#### Stack:
 - Pyhton
 - Django
 - Django REST Framework
 - PostgreSQL
 - Redis
 - Celery

Additional libraries are specified in the `requirements.txt` file.

## Project Setup on Windows

### - Installing the Stack
To begin, install: [Python](https://www.python.org/downloads/) | [PostgreSQL](https://www.postgresql.org/) | [Redis](https://redis.io/)
<br>
Links are provided to the latest version of the tools.

### - Cloning a Project from GitHub
Create a root directory on your computer, then open it in your code editor or terminal.
<br>
Next, write this command into the command line:
```powershell
git clone https://github.com/S0fft/SyCloth-Shop.git .
```
You will see the project files appear in your directory.

### - Creating a Virtual Environment
Create a virtual environment:
```powershell
python -m venv .venv
```

And activate it:

```powershell
.venv\Scripts\Activate
``` 
### - Installing the Requirements
Next, install packages:

```powershell
python.exe -m pip install --upgrade pip
``` 
```powershell
pip install -r requirements.txt
```

 ### - Applying the Migrations and Fixture
Using Migrations to Create a Database Structure. Load data from fixture for products and appearance other information.

```powershell
python manage.py migrate
```

```powershell
python manage.py loaddata <path_to_fixture_files>
```

### - Starting Redis and Celery
After, launch Redis and Celery using these commands:

```powershell
redis-server
```

```powershell
celery -A store worker --loglevel=INFO
```
### - Running the Server
Then, run server:
```powershell
python manage.py runserver
```
After starting the server, you can access the application by navigating to `http://127.0.0.1:8000` in your browser.

<details>
<summary><h3> Project Setup on Unix-Like Systems </h3></summary>
These commands do the same thing as described above: 
<br>

### - Installing the Stack
To begin, install: [Python](https://www.python.org/downloads/) | [PostgreSQL](https://www.postgresql.org/) | [Redis](https://redis.io/)
<br>
Links are provided to the latest version of the tools.

### - Cloning a Project from GitHub
Create a root directory on your computer, then open it in your code editor or terminal.
<br>
Next, write this command into the command line:
```powershell
git clone https://github.com/S0fft/SyCloth-Shop.git
```
You will see the project files appear in your directory.

### - Creating a Virtual Environment
```bash
python3 -m pip install --upgrade pip
```

```bash
source ./venv/bin/activate
```

### - Installing the Requirements
```bash
pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

### - Applying the Migrations and Fixture
```bash
python3 manage.py migrate
```

```bash
python3 manage.py loaddata <path_to_fixture_files>
```

### - Starting Redis and Celery
```bash
redis-server
```

```bash
celery -A store worker --loglevel=INFO
```

### - Running the Server
```bash
python3 manage.py runserver
```
After starting the server, you can access the application by navigating to `http://127.0.0.1:8000` in your browser.

</details>
