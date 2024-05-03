FROM python:3.10.14-alpine3.18
LABEL maintainer='p'

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY . /blog
WORKDIR /blog
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

CMD ["/py/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]