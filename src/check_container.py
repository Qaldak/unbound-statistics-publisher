import logging

from python_on_whales import docker, DockerException

logger = logging.getLogger(__name__)


class Container:
    def __init__(self, name):
        self.name = name

    def __log_container_info(self):
        for container in docker.ps(all=True, filters={"name": self.name}):
            logger.debug(f"Container info for '{self.name}': {container.state}")

    def is_running(self):
        try:
            if docker.ps(filters={"name": self.name, "status": "running"}):
                logger.debug(f"Container {self.name} is running")
                return True
            else:
                logger.warning(f"Docker Container '{self.name}' not found or is not running")
                if logger.isEnabledFor(logging.DEBUG):
                    self.__log_container_info()
                return False

        except DockerException as e:
            logger.error(f"{DockerException.__name__}: Exit code {e.return_code}, {e.stderr.strip()}")
