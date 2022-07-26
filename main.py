import time
import indeed_com_scraper as scraper
from dumping import DataDump
from logger import Logger


class ScrapingSession:
    def __init__(self, positions):
        self.positions = positions

    def run(self):
        data_dump = DataDump()
        logger = Logger()

        # scraping -> creates a compiled data dump from different search parameters
        logger.start_session()  # logging start of a session

        for position in self.positions:
            logger.start_scraping(position)  # logging each scraping attempt
            try:
                df = scraper.get_jobs(position)
            except Exception as inst:
                logger.error_occurs(inst)
            else:
                logger.scraping_result(df)  # logging scraping results
                data_dump.merge(df)  # merging all values to the data_dump
            finally:
                time.sleep(5)  # wait for 5 seconds to avoid a block
                continue

        # logging scraping results
        logger.scraping_result_final(data_dump.df)

        # data cleansing / formatting
        data_dump.remove_duplicates(field="job_id")  # removing duplicates

        # logging formatted data dump information
        logger.data_formatted(data_dump.df)

        # saving as a csv file
        data_dump.save_to_csv(path="data_dumps/")

        logger.end_session()
        logger.save_to_txt()  # function is yet to be added
