import os
import sys
import logging
from datetime import datetime


logging_format = "[ %(asctime)s:  module name '%(module)s'  %(levelname)s-%(message)s]"

log_dir = "logs"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_filepath = os.path.join(log_dir,LOG_FILE)
os.makedirs(log_dir, exist_ok=True)


logging.basicConfig(
    level= logging.INFO,
    format= logging_format,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("cc_pred_logger")