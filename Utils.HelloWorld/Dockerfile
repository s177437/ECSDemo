FROM python:3.7.2
WORKDIR /app
COPY . .
RUN pip install pipenv
RUN pipenv install --system --deploy
CMD ["python", "run_me.py"]