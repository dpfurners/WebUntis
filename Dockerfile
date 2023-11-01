FROM python:3.12

ENV PATH = "${PATH}:/chromedriver/chromedriver.exe"


RUN apt-get update && apt-get install -y \
      software-properties-common \
      unzip \
      curl \
      xvfb \
      wget \
          bzip2 \
          snapd

RUN apt install chromium-driver -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
