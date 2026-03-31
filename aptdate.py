import subprocess
import logging
import sys
LOG = "/var/log/aptdate.log"
# an easy app to update my orange pi daily without me touching it. add this bs to crontab and let it go. supposed to be run as root
# run this bs on your risk (you can still run it on RISC)
logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG, encoding="utf-8", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger.debug("Starting APTDATE v0.1")
try: #updating and logging
    subprocess.run (["/usr/bin/apt-get", "update", "-y"], check=True, text=True, capture_output=True) #update package lists
    logger.info ("Package lists updated") #logging to $LOG
except subprocess.CalledProcessError as e: #in case it fucked up, saving a log file
    logger.error ("aptdate FAILED on apt-get update! Error code: %s", e.returncode) #logging to $LOG
    logger.error ("Error: %s", e.stderr) #logging an error output to $LOG
    sys.exit()
try: #upgrading and logging
    subprocess.run (["/usr/bin/apt-get", "upgrade", "-y"], check=True, text=True, capture_output=True) #upgrade the system
    logger.info ("Updated the system") #logging to $LOG
except subprocess.CalledProcessError as e: #in case it fucked up, saving a log file
    logger.error ("aptdate FAILED on apt-get upgrade! Error code: %s", e.returncode) #logging a return code to $LOG
    logger.error ("Error: %s", e.stderr) #logging an error output to $LOG
    sys.exit()
try: #autoremove
    subprocess.run (["/usr/bin/apt-get", "autoremove", "-y"], check=True, text=True, capture_output=True)
    logger.info ("Autoremove complete")
except subprocess.CalledProcessError as e: #in case it fucked up, saving a log file
    logger.error ("aptdate FAILED on apt-get autoremove! Error code: %s", e.returncode)
    logger.error ("Error: %s", e.stderr)
    sys.exit()
try: #cleaning
    subprocess.run (["/usr/bin/apt-get", "clean"], check=True, text=True, capture_output=True)
    logger.info ("Cleaning complete")
except subprocess.CalledProcessError as e: #in case it fucked up, saving a log file
    logger.error ("aptdate FAILED on apt-get clean! Error code: %s", e.returncode)
    logger.error ("Error: %s", e.stderr)
    sys.exit()
