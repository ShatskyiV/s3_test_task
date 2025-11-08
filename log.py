import logging

logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("pytest_logger")
