"""Contains the CsvValidator Class that converts a CSV file into JSON objects whilst 
utilising AssetValidator to validate the data. 

A Log file is created for auditing purposes. If un-needed then remove Lines 17-33
"""
from .asset_validator import AssetValidator as AV
import logging
import os

# Ensure the 'logs' directory exists
# Logging to file for Audit purposes
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set log level to INFO

# Create a file handler and set its level to INFO
log_file_path = os.path.join(log_directory, "logfile.log")
file_logger = logging.FileHandler(log_file_path)
file_logger.setLevel(logging.INFO)

# Create a stream handler to print log messages to the terminal
stream_logger = logging.StreamHandler()
stream_logger.setLevel(logging.INFO)

# Create a formatter and set the formatter for the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_logger.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_logger)
logger.addHandler(stream_logger)


class CsvConverter:
    """Converts asset data from a TFL Asset CSV file to JSON format 
    and extracts bounding box coordinates.

    This class provides methods to read and process asset data from a CSV file. 
    It validates the data, converts valid records to JSON format, 
    and calculates the bounding box of asset coordinates.

    Attributes:
        valid_assets (list): List to store valid Asset objects.
        invalid_assets (list): List to store invalid CSV records.
        bounding_box (dict): Bounding box of asset coordinates.
        json_data (list): List for JSON records.
    """

    @staticmethod
    def asset_to_json(asset: "AV") -> dict:
        """Converts an Asset object to a JSON-compatible dictionary.

        Args:
            asset (AssetValidator): The Asset object to be converted to JSON.
        Returns:
            dict: A dictionary containing the Asset object's data.
        """
        return {
            "ID": asset.asset_id,
            "TYPE": asset.asset_type,
            "TYPE_DESC": asset.type_description,
            "INSTALL_DATE": asset.install_date,
            "EASTING": int(asset.easting),
            "NORTHING": int(asset.northing),
            "LOCATION": asset.location,
            "CELL": asset.cell,
            "SIGNAL_GROUP": asset.signal_group,
            "STATUS": asset.status,
            "INSTALL_ENGINEER": asset.install_engineer,
        }

    def __init__(self):
        """Initializes a CsvConverter object."""
        self.valid_assets = []  # List to store valid Asset objects
        self.invalid_assets = []  # List to store invalid CSV records
        self.bounding_box = None  # Bounding box of asset coordinates
        self.json_data = []  # List for JSON records.

    def process_csv_file(self, file_path: str) -> tuple:
        """
        Reads and processes asset data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.
        Returns:
            tuple: A tuple containing valid asset data in JSON format, bounding box coordinates, 
            and a list of invalid CSV records that weren't processed.
        Raises:
            TypeError: If the input file is not a CSV file.
            ValueError: If the CSV file headers are incorrect.
        """
        count = 0
        # CSV Check
        if file_path.split(".")[-1] != "csv":
            raise TypeError("Input file is not a CSV")

        header_line = None  # Variable to store the header line
        with open(file_path, "r", encoding="utf-8") as csv_file:
            # Validate columns names against expected headers and process.
            for line_number, line in enumerate(csv_file):
                if line_number == 0:  # First line, assumed to be headers.
                    header_line = line.strip().split(
                        ","
                    )  # Relies on ',' deliminated. Check deliminater in file if ValueError raised.
                    expected_headers = [
                        "ID",
                        "TYPE",
                        "TYPE_DESC",
                        "INSTALL_DATE",
                        "EASTING",
                        "NORTHING",
                        "LOCATION",
                        "CELL",
                        "SIGNAL_GROUP",
                        "STATUS",
                        "INSTALL_ENGINEER",
                    ]
                    if header_line != expected_headers:
                        logger.error(
                            f"CSV headers are '{header_line}'"
                        )  # Log failed headers.
                        raise ValueError("Error: Incorrect headers in the CSV file.")
                else:
                    csv_record = line.strip().split(",")
                    count += 1
                    try:
                        asset = AV.from_csv_record(csv_record)
                        self.valid_assets.append(asset)
                    except Exception as e:
                        # Log invalid records.
                        # Add to a list of invalid records for future interrogation.
                        logger.error(f"Invalid record {csv_record[0]}: {e}")
                        self.invalid_assets.append( 
                            csv_record
                        ) # Embedded list for visual clarity.
                        pass

        logger.info(
            f"{count} assets processed. Of which, {len(self.invalid_assets)} are invalid. Please check logs for further information."
        )
        logger.info("")  # Added for clarity. Remove depending on processing frequency.
        logger.info(
            "-----------------------------------------------------------------------------"
        )
        logger.info("")

        # Calculate bounding box
        if self.valid_assets:
            northings = [(asset.northing) for asset in self.valid_assets]
            eastings = [(asset.easting) for asset in self.valid_assets]
            self.bounding_box = {
                "min_northing": min(northings),
                "max_northing": max(northings),
                "min_easting": min(eastings),
                "max_easting": max(eastings),
            }

        # Convert valid assets to JSON format
        self.json_data = [
            CsvConverter.asset_to_json(asset) for asset in self.valid_assets
        ]

        return self.json_data, self.bounding_box, self.invalid_assets
