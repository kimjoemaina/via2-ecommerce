FROM python:3.10.12-alpine3.18

RUN pip install --upgrade pip

WORKDIR /via2

COPY requirements.txt .

RUN apk update && apk upgrade \
    && apk add gcc mariadb-dev musl-dev pkgconf \
    && apk add --no-cache build-base linux-headers

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

ENTRYPOINT [ "sh", "entrypoint.sh" ]