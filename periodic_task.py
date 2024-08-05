import threading
import os
import subprocess as sp
from dotenv import load_dotenv
import logging
import datetime


logging.basicConfig(level=logging.INFO)
load_dotenv()

def check_squid_status():
    try:
        # Check the status of the squid service
        result = sp.run(['service', 'squid', 'status'], check=True, stdout=sp.PIPE, stderr=sp.PIPE)
        logging.info("Squid service is running.")
    except sp.CalledProcessError:
        logging.info("Squid service is not running. Restarting the service...")
        try:
            # Restart the squid service if the status check fails
            restart_result = sp.run(['service', 'squid', 'restart'], check=True, stdout=sp.PIPE, stderr=sp.PIPE)
            logging.info("Squid service restarted successfully.")
        except sp.CalledProcessError as restart_error:
            logging.error(f"Failed to restart squid service: {restart_error}")


def update_reports():
    time = datetime.datetime.now()
    logging.info(f"updating internet logs at {time}")
    sp.call(['sarg'])
    sp.call(['nginx','-s','reload'])
    check_squid_status()
    t = threading.Timer(int(os.getenv("PERIDIC_TASK_RUN")),update_reports)
    t.start()

def run():
    update_reports()

sp.call(['service','nginx','restart'])
run()
