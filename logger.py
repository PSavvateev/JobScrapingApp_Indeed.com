"""
module with functionality of the logging the results of the program run.
"""
from datetime import datetime


def get_time():
    return datetime.now().strftime('%d-%m-%Y, %H:%M:%S')


def logging(time, message, logs_lst):
    log = (time, message)
    logs_lst.append(log)
    print(time + ': ' + message)


class Logger:
    def __init__(self):
        self.logs_lst = []

    def start_session(self):
        time = get_time()
        message = "Session starts"
        logging(time, message, self.logs_lst)

    def end_session(self):
        time = get_time()
        message = "Session ends."
        logging(time, message, self.logs_lst)

    def start_scraping(self, position):
        time = get_time()
        message = f"Scraping attempt with the key word: '{position}'... "

        logging(time, message, self.logs_lst)

    def scraping_result(self, df):
        time = get_time()
        message = f"....successfully implemented. Number of records found: {len(df)}"
        logging(time, message, self.logs_lst)

    def scraping_result_final(self, df):
        time = get_time()
        message = f"Full scraping is executed. The raw data dump file contains {len(df)} records.\n" \
                  f"Number of unique records is {df['job_id'].nunique()}."
        logging(time, message, self.logs_lst)

    def data_formatted(self, df):
        time = get_time()
        message = f"Data dump is formatted:\n {df.info()}"
        logging(time, message, self.logs_lst)

    def error_occurs(self, error):
        time = get_time()
        message = f"{error} occurs"
        logging(time, message, self.logs_lst)

    def save_to_txt(self):
        pass
