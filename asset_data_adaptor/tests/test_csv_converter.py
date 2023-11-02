"""
This module contains unit tests for the CsvConverter class and its associated methods.

The CsvConverter class is responsible for processing CSV files containing asset data and converting it to JSON format.

Classes:
    TestCsvConverter(unittest.TestCase): A class containing unit tests for the CsvConverter class.
Methods:
    test_asset_to_json: Test case to validate the conversion of AssetValidator objects to JSON format.
    test_process_csv_file_valid: Test case to validate the processing of a valid CSV file.
    test_process_csv_file_invalid: Test case to validate the processing of an invalid CSV file.
    test_process_csv_file_non_csv_file: Test case to validate handling non-CSV files.
    test_process_csv_file_incorrect_headers: Test case to validate handling incorrect CSV headers.
"""

import unittest
from unittest.mock import patch
from ..asset_csv_converter.asset_validator import AssetValidator as AV
from ..asset_csv_converter.csv_converter import CsvConverter


class TestCsvConverter(unittest.TestCase):
    """
    Unit tests for the CsvConverter class.
    """

    def setUp(self):
        """
        Set up a CsvConverter instance for testing.
        """
        self.converter = CsvConverter()

    VALID_CSV_RECORD = (
        "12/345678",
        "DC",
        "Dual Toucan",
        "10-Apr-2023",
        "531695",
        "181465",
        "Valid Location",
        "NORT",
        "R801",
        "Active",
        "Valid Engineer",
    )
    EXPECTED_JSON = {
        "ID": "12/345678",
        "TYPE": "DC",
        "TYPE_DESC": "Dual Toucan",
        "INSTALL_DATE": "10-Apr-2023",
        "EASTING": 531695,
        "NORTHING": 181465,
        "LOCATION": "Valid Location",
        "CELL": "NORT",
        "SIGNAL_GROUP": "R801",
        "STATUS": "Active",
        "INSTALL_ENGINEER": "Valid Engineer",
    }

    def test_asset_to_json(self):
        """
        Test case to validate the conversion of AssetValidator objects to JSON format.
        """
        asset = AV(
            asset_id="12/345678",
            asset_type="DC",
            type_description="Dual Toucan",
            install_date="10-Apr-2023",
            easting="531695",
            northing="181465",
            location="Valid Location",
            cell="NORT",
            signal_group="R801",
            status="Active",
            install_engineer="Valid Engineer",
        )

        self.assertEqual(
            CsvConverter.asset_to_json(asset), TestCsvConverter.EXPECTED_JSON
        )

    @patch("builtins.open", create=True)
    def test_process_csv_file_valid(self, mock_open):
        """
        Test case to validate the processing of a valid CSV file.
        """
        mock_file = mock_open.return_value
        mock_file.__enter__.return_value = [
            "ID,TYPE,TYPE_DESC,INSTALL_DATE,EASTING,NORTHING,LOCATION,CELL,SIGNAL_GROUP,STATUS,INSTALL_ENGINEER",
            "12/345678,DC,Dual Toucan,10-Apr-2023,531695,181465,Valid Location,NORT,R801,Active,Valid Engineer",
        ]

        json_data, bounding_box, invalid_assets = self.converter.process_csv_file(
            "test.csv"
        )

        expected_json_data = [TestCsvConverter.EXPECTED_JSON]

        expected_bounding_box = {
            "min_northing": f"{TestCsvConverter.EXPECTED_JSON['NORTHING']}",
            "max_northing": f"{TestCsvConverter.EXPECTED_JSON['NORTHING']}",
            "min_easting": f"{TestCsvConverter.EXPECTED_JSON['EASTING']}",
            "max_easting": f"{TestCsvConverter.EXPECTED_JSON['EASTING']}",
        }

        self.assertEqual(json_data, expected_json_data)
        self.assertEqual(bounding_box, expected_bounding_box)
        self.assertEqual(invalid_assets, [])

    @patch("builtins.open", create=True)
    def test_process_csv_file_invalid(self, mock_open):
        """
        Test case to validate the processing of an invalid CSV file.
        """
        mock_file = mock_open.return_value
        mock_file.__enter__.return_value = [
            "ID,TYPE,TYPE_DESC,INSTALL_DATE,EASTING,NORTHING,LOCATION,CELL,SIGNAL_GROUP,STATUS,INSTALL_ENGINEER",
            "12/34567,D,Dual Toucan,10-pr-2023,53195,18165,Valid Location,NORT,R801,Active,Valid Engineer",
        ]

        json_data, bounding_box, invalid_assets = self.converter.process_csv_file(
            "test.csv"
        )

        self.assertEqual(json_data, [])
        self.assertEqual(bounding_box, None)
        self.assertEqual(
            invalid_assets,
            [
                [
                    "12/34567",
                    "D",
                    "Dual Toucan",
                    "10-pr-2023",
                    "53195",
                    "18165",
                    "Valid Location",
                    "NORT",
                    "R801",
                    "Active",
                    "Valid Engineer",
                ]
            ],
        )

    def test_process_csv_file_non_csv_file(self):
        """
        Test case to validate handling non-CSV files.
        """
        with self.assertRaises(TypeError):
            self.converter.process_csv_file("test.txt")

    @patch("builtins.open")
    def test_process_csv_file_incorrect_headers(self, mock_open):
        """
        Test case to validate handling incorrect CSV headers.
        """
        mock_file = mock_open.return_value
        mock_file.__enter__.return_value = ["ID,TYPE,INCORRECT_HEADER\n1,Type,Value"]

        with self.assertRaises(ValueError):
            self.converter.process_csv_file("test.csv")


if __name__ == "__main__":
    unittest.main()
