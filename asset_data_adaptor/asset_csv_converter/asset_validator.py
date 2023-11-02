"""Contains the AssetValidator Class that validates an data from a TFL Asset CSV File.
Validation methods can be expanded depending on use cases. 
Methods should validate in a negative validation order that raises the appropriate Error. 
If the data passes validation then return True. Therefore, the Asset object can be created
after passing appropriate validation methods.
"""

import re
from datetime import datetime


class AssetValidator:
    """
    The AssetValidator class provides methods for validating asset data imported from a TFL Asset CSV file.
    It performs various checks on asset attributes to ensure data integrity and validity.

    Attributes:
        VALID_ASSET_TYPES (dict): A dictionary mapping valid asset type codes to their corresponding descriptions.
        VALID_STATUS_VALUES (list): A list of valid asset status values ('Active', 'Proposed', 'Inactive').
        VALID_CELL_VALUES (list): A list of valid cell values ('NORT', 'EAST', 'CNTR', 'WEST').
    """

    # Constant valid values
    VALID_ASSET_TYPES = {
        "DC": "Dual Toucan",
        "MP": "Junction",
        "P": "Pelican",
        "PD": "Pedestrian",
        "TN": "Toucan",
    }
    VALID_STATUS_VALUES = ["Active", "Proposed", "Inactive"]
    VALID_CELL_VALUES = ["NORT", "EAST", "CNTR", "WEST"]

    def __init__(
        self,
        asset_id: str,
        asset_type: str,
        type_description: str,
        install_date: str,
        easting: str,
        northing: str,
        location: str,
        cell: str,
        signal_group: str,
        status: str,
        install_engineer: str,
    ) -> None:
        """Initializes an Asset object with provided data.

        Args:
            asset_id (str): The unique identifier of the asset.
            asset_type (str): The type code of the asset (e.g., 'DC', 'MP', 'P', 'PD', 'TN').
            type_description (str): The description corresponding to the asset type.
            install_date (str): The installation date of the asset (in the format 'DD-Mon-YYYY').
            easting (str): The easting coordinate of the asset.
            northing (str): The northing coordinate of the asset.
            location (str): The location information of the asset.
            cell (str): The cell information of the asset.
            signal_group (str): The signal group information of the asset.
            status (str): The status of the asset ('Active', 'Proposed', 'Inactive').
            install_engineer (str): The name of the installation engineer.
        """
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.type_description = type_description
        self.install_date = install_date
        self.easting = easting
        self.northing = northing
        self.location = location
        self.cell = cell
        self.signal_group = signal_group
        self.status = status
        self.install_engineer = install_engineer

    @staticmethod
    def _empty_field_check(value: str, field_name: str) -> None:
        """Validates that a given field is not empty or consists only of whitespace characters.

        Args:
            value (str): The field value to be validated.
            field_name (str): The name of the field being validated.
        Raises:
            ValueError: If the field is empty or consists only of whitespace characters.
        """
        if not value or not value.strip():
            raise ValueError(f"The field '{field_name}' cannot be empty. Please check")
        return True

    @staticmethod
    def _validate_asset_id(asset_id: str) -> None:
        """Validates the format of the asset ID and checks its length.

        Args:
            asset_id (str): The asset ID to be validated.
        Raises:
            ValueError: If the asset ID is in an incorrect format or has an incorrect length.
        """
        # Validate ID format using regex pattern
        id_regex_pattern = r"^\d{2}/\d{6}$"
        if not re.match(id_regex_pattern, asset_id):
            raise ValueError(
                f"Invalid format for asset ID: '{asset_id}'. Please check."
            )
        return True

    @staticmethod
    def _validate_asset_type(asset_type: str, type_description: str) -> None:
        """Validates the asset type and its corresponding description.

        Args:
            asset_type (str): The asset type code to be validated.
            type_description (str): The description corresponding to the asset type.
        Raises:
            ValueError: If the asset type value is invalid.
            ValueError: If the type description does not match the corresponding asset type.
        """
        # Check asset type against valid values.
        if asset_type not in AssetValidator.VALID_ASSET_TYPES.keys():
            raise ValueError(f"Invalid asset type value: '{asset_type}'. Please check.")
        # Confirm type description matches type and that it is an allowed value.
        if type_description != AssetValidator.VALID_ASSET_TYPES[asset_type]:
            raise ValueError(
                f"Type description '{type_description}' does not match asset type '{asset_type}'"
            )
        return True

    @staticmethod
    def _validate_status(status: str) -> None:
        """Validates the status of the asset.

        Args:
            status (str): The status of the asset.
        Raises:
            ValueError: If the status is not one of "Active", "Proposed", or "Inactive".
        """

        # Check for invalid value
        if status not in AssetValidator.VALID_STATUS_VALUES:
            raise ValueError(f"Status '{status}' is not a valid option")
        return True

    # TODO re-write docstring
    @staticmethod
    def _validate_install_date(install_date: str, status: str) -> None:
        """Validates the installation date of the asset based on its status.

        Args:
            install_date (str): The installation date of the asset.
            status (str): The status of the asset.
        Raises:
            ValueError: If the date value is not in the following format 'dd-Mon-yyyy'.
            ValueError: If the install date is in the future for an active or inactive site.
        """
        # Reference date
        ref_date = datetime.now()
        # Parse the input install date using datetime.
        try:
            install_date_obj = datetime.strptime(
                install_date, "%d-%b-%Y"
            )  # Regex could be used for tighter control if needed.
        except ValueError:
            raise ValueError(
                f"Install date '{install_date}' is in an invalid date format. Please ensure it is in 'dd-Mon-yyyy'"
            )
        # Validate against reference date
        if status != "Proposed":
            if install_date_obj > ref_date:
                raise ValueError(
                    "Install date is in the future for an active/inactive site. Please check."
                )
        return True

    @staticmethod
    def _validate_easting(easting: str) -> None:
        """Validates the BNG easting coordinate of the asset to ensure they're within the London Area,UK.

        Args:
            easting (str): The easting coordinate to be validated.
        Raises:
            ValueError: If the easting coordinate is not a valid number or out of range.
        """
        # Empty field check
        AssetValidator._empty_field_check(easting, "Easting")
        # Easting range for London Area (BNG)
        max_easting = 538216
        min_easting = 500442
        # Confirm it's a number
        try:
            int_easting = int(easting)
        except Exception as e:
            raise e
        # Validate BNG range for northing
        if max_easting > int_easting < min_easting:
            raise ValueError(
                f"Easting '{easting}' out of range for London Area. Please Check."
            )
        return True

    @staticmethod
    def _validate_northing(northing: str) -> None:
        """Validates the BNG northing coordinate of the asset to ensure they're within the London Area,UK.

        Args:
            easting (str): The northing coordinate to be validated.
        Raises:
            ValueError: If the northing coordinate is not a valid number or out of range.
        """
        # Empty field check
        AssetValidator._empty_field_check(northing, "Northing")
        # Northing range for London Area (BNG)
        max_northing = 205415
        min_northing = 148012
        # Confirm it's a number
        try:
            int_northing = int(northing)
        except Exception as e:
            raise e
        # Validate BNG range for northing
        if max_northing > int_northing < min_northing:
            raise ValueError(
                f"Northing '{northing}' out of range for London Area. Please Check."
            )

        return True

    @staticmethod
    def _validate_location(location: str) -> None:
        """Validates the location field is not empty.

        Args:
            location (str): The location to be validated.
        Raises:
            ValueError: If the location does not meet the required format or constraints.
        """

        # Empty field check
        AssetValidator._empty_field_check(location, "Location")
        return True

    @staticmethod
    def _validate_cell(cell: str) -> None:
        """Validates the cell field values are within the allowed values:
        "NORT","EAST","CNTR","WEST".

        Args:
            cell (str): The cell information to be validated.
        Raises:
            ValueError: If the cell value is not within the allowed values.
        """

        # Check against valid Cell values.
        if cell not in AssetValidator.VALID_CELL_VALUES:
            raise ValueError(f"Invalid value for Cell: '{cell}'. Please check")
        return True

    @staticmethod
    def _validate_signal_group(signal_group: str) -> None:
        """Validates that signal group values adhere to the following format: 
        Begin with G/R followed by digits.

        Args:
            signal_group (str): The signal group information to be validated.
        Raises:
            ValueError: If the signal group information is outside the allowed format.
        """
        # Validate Signal Group using regex pattern
        signal_regex_pattern = r"^(G|R)\d+$"
        if not re.match(signal_regex_pattern, signal_group):
            raise ValueError(
                f"Invalid format for Signal Group: '{signal_group}'. Please check."
            )
        return True

    @staticmethod
    def _validate_engineer(install_engineer: str) -> None:
        """Validates that installation engineer is not an empty field.

        Args:
            install_engineer (str): The installation engineer's name.
        Raises:
            ValueError: If the installation engineer's name is empty.
        """
        # Empty field check
        AssetValidator._empty_field_check(install_engineer, "Install Engineer")
        return True

    @classmethod
    def from_csv_record(cls, csv_record: tuple) -> "AssetValidator":
        """Creates an Asset object from a CSV record.

        Args:
            csv_record (tuple): A tuple containing asset data from a CSV record.
        Returns:
            AssetValidator: An AssetValidator object created from the CSV record.
        Raises:
            ValueError: If the CSV record contains invalid data.
        """
        # Create variables from the csv_record
        (
            asset_id,
            asset_type,
            type_description,
            install_date,
            easting,
            northing,
            location,
            cell,
            signal_group,
            status,
            install_engineer,
        ) = csv_record
        # Validate data fields here using the validation methods
        cls._validate_asset_id(asset_id)
        cls._validate_asset_type(asset_type, type_description)
        cls._validate_status(
            status
        )  # Status before date to ensure the status field is in the correct format.
        cls._validate_install_date(install_date, status)
        cls._validate_easting(easting)
        cls._validate_northing(northing)
        cls._validate_location(location)
        cls._validate_cell(cell)
        cls._validate_signal_group(signal_group)
        cls._validate_engineer(install_engineer)

        # Validate other fields similarly
        return cls(
            asset_id,
            asset_type,
            type_description,
            install_date,
            easting,
            northing,
            location,
            cell,
            signal_group,
            status,
            install_engineer,
        )
