# Example of try-except test using pytest
How to conduct try-except test pattern in pytest

## Assumption
I assume that host environment is satisfied with the following conditions.

| Item  | Detail | Command |
| :---- | :---- | :---- |
| Device | Raspberry Pi 4 Model B Rev 1.4 | `cat /proc/cpuinfo \| sed -e "s/\s\s*/ /g" \| grep -oP "(?<=Model : )(.*)"` |
| Architecture | aarch64 (64bit) | `uname -m` |
| OS | Debian GNU/Linux 11 (bullseye) | `cat /etc/os-release \| grep -oP '(?<=PRETTY_NAME=")(.*)(?=")'` |

## Preparation
1. Install `git`, `docker`, and `docker-compose` to your machine and enable each service.
1. Run the following command and change current directory to the project.

    ```bash
    git clone https://github.com/yuruto-free/pytest-try-except.git
    ```

1. Create `.env` file in the top directory of current project. The `.env` file consists of two environment variables.

    | Environment variable name | Overview | Example |
    | :---- | :---- | :---- |
    | `PYTEST_APP_ARCHI` | architecture name | amd64, arm32v5, arm32v6, arm32v7, arm64v8, etc. |
    | `PYTEST_APP_TZ` | Time Zone | UTC, Asia/Tokyo, etc.

    Please see [`env.sample`](./env.sample) for details.

1. Execute the following commands to build image and start docker containers.

    ```bash
    # Build docker images
    docker-compose build --no-cache --build-arg UID="$(id -u)" --build-arg GID="$(id -g)"

    # Start docker containers
    docker-compose up -d
    ```

## Execute python-test using pytest
To execute python-test, run the following command.

```bash
# ================
# Host environment
# ================
# Enter the container
docker exec -it pytest.try-except bash

# ==================
# Docker environment
# ==================
# Execute pytest
pytest
```