# Use an official Python runtime as a parent image
FROM python:3

ENV TZ="Europe/Paris"

WORKDIR /app

COPY ./requirements.txt ./
COPY ./gen_profile_pic.py ./
COPY ./update_profile.py ./
COPY ./main.py ./
COPY ./fonts/ /app/fonts

RUN apt update && apt install -y python3 python3-pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python file
CMD [ "python3", "./main.py" ]
