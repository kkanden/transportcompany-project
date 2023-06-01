import unittest
from unittest.mock import MagicMock, patch
from packages import Packages


class TestPackages(unittest.TestCase):
    def setUp(self):
        self.packages_file = "C:\\Users\\Gracz\\OneDrive\\Desktop\\GitHub\\transportcompany-project\\unit tests\\kupa.txt"

    @patch("builtins.open")
    def test_create_packages(self, mock_open):
        mock_file = MagicMock()
        mock_file.__enter__.return_value = [
            "P1 A B 06:00",
            "P2 B C 08:00",
            "P3 A C 10:00",
        ]
        mock_open.return_value = mock_file

        with patch("packages.Package") as mock_package:
            packages = Packages(self.packages_file)
            mock_package.assert_has_calls(
                [
                    unittest.mock.call("P1", "A", "B", unittest.mock.ANY),
                    unittest.mock.call("P2", "B", "C", unittest.mock.ANY),
                    unittest.mock.call("P3", "A", "C", unittest.mock.ANY),
                ]
            )

        mock_open.assert_called_once_with(self.packages_file, "r")
        self.assertEqual(len(packages.packages), 3)

    def test_add_package(self):
        packages = Packages(self.packages_file)

        pack_id = "P4"
        start_station = "C"
        end_station = "D"
        time_pack = MagicMock()

        packages.add_package(pack_id, start_station, end_station, time_pack)

        self.assertEqual(len(packages.packages), 4)
        self.assertIn(pack_id, packages.packages)

    def test_get_package(self):
        packages = Packages(self.packages_file)

        pack_id = "P1"
        package = MagicMock()

        packages.packages = {pack_id: package}

        self.assertEqual(packages.get_package(pack_id), package)

    def test_get_packages(self):
        packages = Packages(self.packages_file)

        packages.packages = {"P1": MagicMock(), "P2": MagicMock(), "P3": MagicMock()}

        package_ids = packages.get_packages()

        self.assertEqual(len(package_ids), 3)
        self.assertIn("P1", package_ids)
        self.assertIn("P2", package_ids)
        self.assertIn("P3", package_ids)


if __name__ == "__main__":
    unittest.main()
