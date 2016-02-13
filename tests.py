import unittest

from app import read_config

class ConfigFileReaderTest(unittest.TestCase):
    def test_read(self):
        config = read_config('config')
        self.assertEqual(config['cmus_host'], 'raspberry')
        self.assertEqual(config['cmus_passwd'], 'PaSsWd')
        self.assertEqual(config['app_host'], 'localhost')
        self.assertEqual(config['app_port'], '8080')

if __name__ == '__main__':
    unittest.main()
