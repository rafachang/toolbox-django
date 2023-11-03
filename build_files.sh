# build_files.sh
pip install -r requirements.txt

# make migrations
py manage.py migrate
py manage.py collectstatic
