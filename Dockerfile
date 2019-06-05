FROM python:3.7.3

LABEL maintainer="matchVote <admin@matchvote.com>"
LABEL version="0.2.0"

RUN apt-get update \
  && apt-get install -y postgresql-client \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m dogood
USER dogood

# Download NLTK dependencies - must be after user is set
RUN python -m nltk.downloader punkt

COPY . /usr/src/app

CMD ["bin/start"]
