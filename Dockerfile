FROM python:3.9-slim

# Install required system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        curl \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install ViennaRNA
WORKDIR /viennarna
RUN wget https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_4_x/ViennaRNA-2.4.18.tar.gz \
    && tar -xzf ViennaRNA-2.4.18.tar.gz \
    && cd ViennaRNA-2.4.18 \
    && ./configure \
    && make \
    && make install \
    && rm -rf /viennarna

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
