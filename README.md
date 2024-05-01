Project "Blog" preview:

...

Installing "Blog" project on Linux:

git clone git@github.com:ppenkovskiy/blog.git

cd blog

sudo apt install python3.10-venv

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver