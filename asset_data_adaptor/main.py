from asset_csv_converter.csv_converter import CsvConverter

# Example usage:
if __name__ == "__main__":
    # Replace with the actual path to your CSV file
    csv_file_path = r"..\Data for Python Programming Exercise.csv"
    converter = CsvConverter()
    json_data, bounding_box, invalid_assets = converter.process_csv_file(csv_file_path)
    print("Valid Assets (JSON Format):")
    print(json_data)
    print("Bounding Box:")
    print(bounding_box)
    print("Invalid Assets")
    print(invalid_assets)
