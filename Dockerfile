FROM python:3.9.18

WORKDIR /home
RUN mkdir /home/api
RUN apt update && apt upgrade -y && apt install -y ffmpeg

ENV HOME /home
COPY . /home/api
WORKDIR /home/api
RUN pip install poetry
RUN poetry install --no-root

EXPOSE 8080

CMD ["poetry", "run", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
