FROM python:3.7-stretch

WORKDIR /app
COPY . .
RUN pip install -r requirements

# RUN ["python", "manage.py", "migrate"]
# # echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell
# EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080"]