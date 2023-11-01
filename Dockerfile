FROM python:3.11

ENV PATH = "${PATH}:/chromedriver/chromedriver.exe"


RUN apt-get update && apt-get install -y \
      software-properties-common \
      unzip \
      curl \
      xvfb \
      wget \
          bzip2 \
          snapd

# Chrome
# RUN apt-get update && \
#     apt-get install -y gnupg wget curl unzip --no-install-recommends && \
#     wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
#     apt-get update -y && \
#     apt-get install -y google-chrome-stable && \
#     wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip" && \
#     unzip /chromedriver/chromedriver* -d /chromedriver

RUN apt install chromium-driver -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
