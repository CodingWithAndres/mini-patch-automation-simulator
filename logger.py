import logging

logging.basicConfig(
    filename="patch.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_success(server):
    logging.info(f"Patch successful on {server}")

def log_failure(server):
    logging.error(f"Patch FAILED on {server}")
