FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    lsb-release \
    gnupg2 \
    bash-completion \
    && curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash -x \
    && echo 'export PATH=$PATH:/root/yandex-cloud/bin' >> /etc/profile \
    && ln -s /root/yandex-cloud/bin/yc /usr/local/bin/yc \
    && apt-get clean

WORKDIR /app_code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]