ARG PYTHON_VERSION=3.12

FROM alpine AS python-builder
ARG PYTHON_VERSION

RUN apk add --no-cache python3~=${PYTHON_VERSION}
WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN python -m compileall -o 2 .
RUN find . -name "*.cpython-*.opt-2.pyc" | awk '{print $1, $1}' | sed 's/__pycache__\///2' | sed 's/.cpython-[0-9]\{2,\}.opt-2//2' | xargs -n 2 mv
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +


FROM python:3.12.5-alpine3.20 AS app-builder

COPY requirements.txt ./
RUN pip install --no-cache-dir --no-cache -r requirements.txt

RUN pip uninstall -y setuptools pip wheel


FROM scratch
ARG PYTHON_VERSION

COPY --from=python-builder /usr/bin/python3 /
COPY --from=python-builder /lib/ld-musl-*.so.1 /lib/
COPY --from=python-builder /lib/libz.so.1 /lib/
COPY --from=python-builder /usr/lib/libffi.so.8 /usr/lib/
COPY --from=python-builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/libpython${PYTHON_VERSION}.so.1.0
COPY --from=python-builder /usr/lib/python${PYTHON_VERSION}/ /usr/lib/python${PYTHON_VERSION}/
COPY --from=app-builder /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/lib/python${PYTHON_VERSION}/site-packages/

WORKDIR /app
COPY src ./

CMD ["/python3", "/app/main.py"]
