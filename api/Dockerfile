FROM python:3.9.18

WORKDIR /home
RUN mkdir /home/api
RUN apt update && apt upgrade -y && apt install -y ffmpeg

ENV HOME /home
COPY . /home/api
WORKDIR /home/api
RUN pip install poetry
RUN poetry install --no-root
# WORKDIR /home/root-user

# # Build essential
# RUN apt-get update && apt-get upgrade -y && apt-get install -y \
#     build-essential \
#     curl \
#     git \
#     wget \
#     make \

# RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# ENV PYENV_ROOT $HOME/.pyenv
# ENV PATH $PYENV_ROOT/bin:$PATH

# Python installation
# RUN apt-get install -y python3.10
# WORKDIR /home/pip
# RUN wget https://bootstrap.pypa.io/get-pip.py

# Pip installation
# RUN python3 get-pip.py

# Poetry installation
# RUN pip install poetry


# Poetry installation
EXPOSE 8080

CMD ["poetry", "run", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
