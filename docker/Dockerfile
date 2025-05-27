ARG ARCHITECTURE=arm64v8

From ${ARCHITECTURE}/python:3.12.10-alpine3.21
ARG UID
ARG GID
ARG USERNAME=user
ARG GROUPNAME=user
ARG TZ=Asia/Tokyo
ENV APP_ROOT_PATH=/opt/app

LABEL maintainer="yuruto-free"
LABEL description="Build pytest environment"

COPY ./pyproject.toml /opt/pyproject.toml
COPY ./waiting.sh /opt/waiting.sh

RUN    apk update \
    && apk upgrade \
    \
    # Install mandatory libraries
    \
    && apk add --no-cache bash tzdata \
    \
    # Install relevant libraries for development
    \
    && apk add --no-cache gcc musl-dev libffi-dev g++ libgcc libstdc++ libxslt-dev \
                          python3-dev libc-dev linux-headers curl shadow \
    && ln -s /usr/share/zoneinfo/${TZ} /etc/localtime \
    && pip install --upgrade setuptools \
    && pip install poetry \
    && groupadd -g ${GID} ${GROUPNAME} \
    && useradd --shell /bin/bash --no-log-init --create-home --home-dir /opt/home --gid ${GID} --uid ${UID} ${USERNAME} \
    && mkdir -p ${APP_ROOT_PATH} \
    && chown -R ${USERNAME}:${GROUPNAME} /opt/home \
    && cd /opt \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && chown -R ${USERNAME}:${GROUPNAME} /opt/poetry.lock \
    && chmod 755 /opt/waiting.sh \
    && cd / \
    && rm -rf /root/.cache /var/cache/apk/* /tmp/*

WORKDIR ${APP_ROOT_PATH}
USER ${USERNAME}

CMD ["/opt/waiting.sh"]