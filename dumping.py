"""
Functionality for transforming scraping results into a data-dump ready to be uploaded to a DB or saved to .csv
"""
from datetime import datetime
import pandas as pd


class DataDump:
    def __init__(self):
        self.df = pd.DataFrame()

    def merge(self, df):
        """
        Concatenates new df to the datadump

        :param df: pd.DataFrame
        :return: None
        """
        if len(self.df) != 0:
            self.df = pd.concat(objs=[self.df, df])
        else:
            self.df = df

    def remove_duplicates(self, field):
        """
        Removes duplicates from a df by the 'JobID' field.

        :return: None
        """
        self.df.sort_values(by=field, inplace=True)
        self.df.drop_duplicates(subset=[field], keep="first", inplace=True)

    def format_salaries(self, field):
        self.df[field] = self.df[field].astype("string")

    def save_to_csv(self, path=None):
        """
        Saves a DataFrame into CSV file
        :param path: string
        :return: None
        """
        suffix = datetime.now().strftime("%d%m%Y_%H%M%S")
        file_name = f"datadump_{suffix}.csv"
        self.df.to_csv(path + file_name, index=False)
