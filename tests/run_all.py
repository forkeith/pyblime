import unittest
from pathlib import Path

loader = unittest.TestLoader()
start_dir = str(Path(__file__).parent.resolve())
print(start_dir)
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)
