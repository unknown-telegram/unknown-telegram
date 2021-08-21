FROM python:slim

RUN apt update && apt install -y --no-install-recommends \
    git neofetch && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip3 install --no-warn-script-location --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "-m", "unknown-telegram", "-docker"]