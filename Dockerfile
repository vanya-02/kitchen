FROM python:3.8
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir Flask requests

ENV SRC_DIR /usr/bin/src/webapp/src
COPY src/* ${SRC_DIR}/
WORKDIR $SRC_DIR
COPY src/data/ ./data
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["python", "main.py"]