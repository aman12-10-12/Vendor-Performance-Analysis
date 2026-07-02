import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine("sqlite:///inventory.db")


def ingest_db(df, table_name, engine):
    """
    This function will ingest the dataframe into a database table.
    """
    try:
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        logging.info(f"Successfully ingested '{table_name}' into the database.")
    except Exception as e:
        logging.error(f"Error while ingesting '{table_name}': {e}", exc_info=True)
        raise


def load_raw_data():
    """
    This function loads all CSV files as DataFrames and ingests them into the database.
    """
    start = time.time()

    try:
        for file in os.listdir("data/"):

            if file.endswith(".csv"):
                try:

                    logging.info(f"Reading file: {file}")

                    df = pd.read_csv('data/' + file)

                    logging.info(f"Ingesting {file} into the database.")

                    ingest_db(df, file[:-4], engine)

                except Exception as e:
                    logging.error(
                        f"Failed to process file '{file}': {e}",
                        exc_info=True
                    )

        logging.info("---------------- Ingestion Complete ----------------")

    except Exception as e:
        logging.critical(
            f"Unexpected error during data ingestion: {e}",
            exc_info=True
        )

    finally:
        end = time.time()
        total_time = (end - start) / 60
        logging.info(f"Total Time Taken: {total_time:.2f} minutes")


if __name__ == "__main__":
    load_raw_data()