FROM python:3.10-slim-buster

# Указываем рабочую директорию внутри docker образа
WORKDIR /app

# Копируем всё содержимое текущей папки
COPY . .
COPY requirements.txt .

# Устанавливаем необходимые пакеты python из requirements.txt
# RUN set -xe \
#    && apt-get update \
#    && apt-get install python3 -y \
#    && apt-get install python3-pip -y

RUN pip3 install --no-cache-dir -r requirements.txt

# Запускаем наше Flask приложение командой `python3 -m flask run --host=0.0.0.0`
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
# CMD ["flask", "run", "--host=0.0.0.0"]