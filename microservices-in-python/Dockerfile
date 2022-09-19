FROM python:3.10-alpine3.16
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src src
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
CMD curl -f http://localhost:5000/health || exit 1
EXPOSE 5000
ENTRYPOINT ["python3", "./src/app.py"]
