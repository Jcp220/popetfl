import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("asset_data_adaptor.tests")
    runner = unittest.TextTestRunner()
    runner.run(suite)
