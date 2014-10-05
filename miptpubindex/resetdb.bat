python manage.py flush --noinput
python manage.py makemigrations mpicore ruparser --noinput --merge > resetdb.log
python manage.py migrate --noinput > resetdb.log
python manage.py testdata > resetdb.log