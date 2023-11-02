FROM python:3.10-slim-buster

# Указываем рабочую директорию внутри docker образа
# (там будут расположены все файлы нашего проекта)
WORKDIR /app

# Копируем всё содержимое текущей папки (в которой располагается наш проект)
# в ту папку, которую мы ранее выделили как WORKDIR
COPY . .
COPY requirements.txt .

# Устанавливаем все необходимые пакеты python из requirements.txt
RUN set -xe \
    && apt-get update \
    && apt-get install python3 -y \
    && apt-get install python3-pip -y

RUN pip3 install --no-cache-dir -r requirements.txt

# Запускаем наше Flask приложение командой `python3 -m flask run --host=0.0.0.0`
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
# CMD ["flask", "run", "--host=0.0.0.0"]