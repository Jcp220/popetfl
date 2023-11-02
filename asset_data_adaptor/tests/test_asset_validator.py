"""
This module contains unit tests for the AssetValidator class and its associated methods.
The AssetValidator class is responsible for validating asset data from CSV records.

Classes:
    TestAsset(unittest.TestCase): A class containing unit tests for the AssetValidator class.
Methods:
    test_valid_asset_id: Test case to validate the validation of a valid asset ID.
    test_valid_asset_type: Test case to validate the validation of a valid asset type and type description.
    test_valid_status: Test case to validate the validation of a valid asset status.
    test_valid_install_date: Test case to validate the validation of a valid installation date.
    test_valid_easting: Test case to validate the validation of a valid easting value.
    test_valid_northing: Test case to validate the validation of a valid northing value.
    test_valid_location: Test case to validate the validation of a valid location.
    test_valid_cell: Test case to validate the validation of a valid cell value.
    test_valid_signal_group: Test case to validate the validation of a valid signal group.
    test_valid_engineer: Test case to validate the validation of a valid engineer name.
    test_valid_csv_record: Test case to validate the conversion of a valid CSV record to AssetValidator object.
    test_invalid_csv_record: Test case to validate handling of invalid CSV records.
"""

import unittest
from ..asset_csv_converter.asset_validator import AssetValidator as AV


class TestAsset(unittest.TestCase):
    """
    Unit tests for the AssetValidator class.
    """

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

    def assert_error_cases(self, validation_method, error_cases):
        """
        Helper method to assert that a validation method raises a ValueError for invalid cases.

        Args:
            validation_method (function): The validation method to be tested.
            error_cases (list): List of invalid values to be tested.

        Raises:
            AssertionError: If the validation method does not raise ValueError for any of the error cases.
        """
        for invalid_value in error_cases:
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(
                    ValueError, msg=f"Testing Value Error on {invalid_value}"
                ):
                    validation_method(invalid_value)

    def test_valid_asset_id(self):
        """
        Test case to validate the validation of a valid asset ID.
        """
        # Positive scenario
        self.assertTrue(AV._validate_asset_id("12/123456"))
        # Invalid formats/Negative Scenario
        invalid_ids = [
            "1234567890",
            "12/12345",
            "12|1234567",
            "12/12345",
            "0/123456",
            "12/1234567",
        ]
        TestAsset.assert_error_cases(self, AV._validate_asset_id, invalid_ids)

    def test_valid_asset_type(self):
        """
        Test case to validate the validation of a valid asset type and type description.
        """
        # Positive scenarios
        self.assertTrue(AV._validate_asset_type("DC", "Dual Toucan"))
        # Invalid formats/Negative Scenario
        with self.assertRaises(ValueError):
            AV._validate_asset_type("XX", "Dual Toucan")  # Invalid asset type
            AV._validate_asset_type("DC", "Invalid Type")  # Invalid type description

    def test_valid_status(self):
        """
        Test case to validate the validation of a valid asset status.
        """
        # Positive scenarios
        for valid_value in AV.VALID_STATUS_VALUES:
            self.assertTrue(AV._validate_status(valid_value))
        # Invalid formats/Negative Scenario
        invalid_status_values = ["", "Unknown", "Propose"]
        TestAsset.assert_error_cases(self, AV._validate_status, invalid_status_values)

    def test_valid_install_date(self):
        """
        Test case to validate the validation of a valid installation date.
        """
        # Positive scenarios
        self.assertTrue(
            AV._validate_install_date("29-Jan-2030", "Proposed"),
            msg="AssertTrue on future date, proposed installation",
        )
        self.assertTrue(
            AV._validate_install_date("29-Jan-2001", "Active"),
            msg="AssertTrue on date, active installation",
        )
        self.assertTrue(
            AV._validate_install_date("29-Jan-2001", "Inactive"),
            msg="AssertTrue on date, Inactive installation",
        )

        # Invalid formats/Negative Scenario
        invalid_dates = ["32-Jan-2023", "", "03-Jan-2026"]
        with self.assertRaises(ValueError):
            AV._validate_install_date("03-Jan-2026", "Active")  # Invalid future date
            AV._validate_install_date("32-Jan-2023", "Active")  # Invalid date
            AV._validate_install_date("", "Active")  # Invalid format
            AV._validate_install_date("32-Jan-2026", "Inactive")  # Invalid future date

    def test_valid_easting(self):
        """
        Test case to validate the validation of a valid easting value.
        """
        # Positive scenario
        self.assertTrue(AV._validate_easting("531695"))
        # Invalid formats/Negative Scenario
        with self.assertRaises(ValueError):
            AV._validate_easting("Invalid")  # Invalid format
            AV._validate_easting("123456")  # Invalid range

    def test_valid_northing(self):
        """
        Test case to validate the validation of a valid northing value.
        """
        # Positive scenario
        self.assertTrue(AV._validate_northing("181465"))
        # Invalid formats/Negative Scenario
        with self.assertRaises(ValueError):
            AV._validate_northing("Invalid")  # Invalid format
            AV._validate_northing("654321")  # Invalid range

    def test_valid_location(self):
        """
        Test case to validate the validation of a valid location.
        """
        # Positive scenario
        self.assertTrue(AV._validate_location("London Street"))
        # Invalid format/Negative Scenario
        with self.assertRaises(ValueError):
            AV._validate_location("")  # Empty location

    def test_valid_cell(self):
        """
        Test case to validate the validation of a valid cell value.
        """
        # Positive scenarios
        for cell_value in AV.VALID_CELL_VALUES:
            self.assertTrue(AV._validate_cell(cell_value))
        # Invalid formats/Negative Scenario
        invalid_cell_values = ["", "Unknown", "CnTR"]
        TestAsset.assert_error_cases(self, AV._validate_cell, invalid_cell_values)

    def test_valid_signal_group(self):
        """
        Test case to validate the validation of a valid signal group.
        """
        # Positive scenarios
        valid_signal_values = ["R12", "G1"]
        for valid_value in valid_signal_values:
            self.assertTrue(
                AV._validate_signal_group(valid_value), msg=f"Testing {valid_value}"
            )

        # Invalid formats/Negative Scenario
        invalid_signal_values = ["", "2", "G", "X12"]
        TestAsset.assert_error_cases(
            self, AV._validate_signal_group, invalid_signal_values
        )

    def test_valid_engineer(self):
        """
        Test case to validate the validation of a valid engineer name.
        """
        # Positive scenario
        self.assertTrue(AV._validate_engineer("Jane Smith"))
        # Invalid format/Negative Scenario
        with self.assertRaises(ValueError):
            AV._validate_engineer("")  # Empty engineer name

    def test_valid_csv_record(self):
        """
        Test case to validate the conversion of a valid CSV record to AssetValidator object.
        """
        asset = AV.from_csv_record(TestAsset.VALID_CSV_RECORD)
        self.assertIsInstance(asset, AV)

    def test_invalid_csv_record(self):
        """
        Test case to validate handling of invalid CSV records.
        """
        invalid_csv_records = [
            (
                "12/123456",
                "XX",
                "Invalid Type",
                "32-Jan-2023",
                "123456",
                "654321",
                "London",
                "Nort",
                "GroupA",
                "Unknown",
                "",
            )
        ]
        with self.assertRaises(ValueError):
            for record in invalid_csv_records:
                AV.from_csv_record(record)


if __name__ == "__main__":
    unittest.main()
