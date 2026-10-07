cd pixel_todo
python -m venv venv
source venv/bin/activate          # Linux/Mac
# или venv\Scripts\activate       # Windows
pip install -r requirements.txt
python manage.py makemigrations users tasks battle
python manage.py migrate
python manage.py createsuperuser  # необязательно (админка есть, но не обязательна)
python manage.py runserver
