import unittest
import datetime as dt
from unittest.mock import MagicMock
from driver import Driver

class TestDriver(unittest.TestCase):
    def setUp(self):
        self.stationnet = MagicMock()
        self.stationnet.stat_list = {
            'A': MagicMock(),
            'B': MagicMock(),
            'C': MagicMock()
        }
        self.driver = Driver('D1', self.stationnet)
        self.driver.current_station = self.stationnet.stat_list['A']
        self.driver.clock = dt.timedelta(hours=6, minutes=0)
        self.driver.work_time_remaining = dt.timedelta(hours=8)
        self.driver.packages_delivered = 0
        self.driver.itinerary = []
    
    def test_can_travel_to(self):
        self.driver.current_station.distance_to = MagicMock(return_value=120)
        self.assertTrue(self.driver.can_travel_to('B'))
        
        self.driver.current_station.distance_to = MagicMock(return_value=600)
        self.assertFalse(self.driver.can_travel_to('C'))
    
    def test_can_travel_anywhere(self):
        self.driver.current_station.distances = {
            'B': 120,
            'C': 600
        }
        self.driver.can_travel_to = MagicMock(return_value=True)
        self.assertTrue(self.driver.can_travel_anywhere())
        
        self.driver.can_travel_to = MagicMock(return_value=False)
        self.assertFalse(self.driver.can_travel_anywhere())
    
    def test_pass_time(self):
        self.driver.pass_time(30)
        self.assertEqual(self.driver.clock, dt.timedelta(hours=6, minutes=30))
        self.assertEqual(self.driver.work_time_remaining, dt.timedelta(hours=7, minutes=30))
    
    def test_take_package(self):
        pack = MagicMock()
        self.driver.current_station.available_packages = [pack]
        self.driver.take_package(pack)
        self.assertEqual(len(self.driver.current_station.available_packages), 0)
    
    def test_travel_to(self):
        self.driver.current_station.distance_to = MagicMock(return_value=120)
        self.stationnet.get_station = MagicMock(return_value=self.stationnet.stat_list['B'])
        self.driver.travel_to('B')
        self.assertEqual(self.driver.current_station, self.stationnet.stat_list['B'])
        self.assertEqual(self.driver.clock, dt.timedelta(hours=6, minutes=120))
        self.assertEqual(self.driver.work_time_remaining, dt.timedelta(hours=6, minutes=0))
    
    def test_pickup_and_travel(self):
        pack = MagicMock()
        pack.id = 'P1'
        pack.end_station = 'B'
        pack.time_available = dt.timedelta(hours=7, minutes=0)
        self.driver.current_station.available_packages = [pack]
        self.driver.clock_print = MagicMock(return_value='6:00')
        self.driver.pickup_and_travel()
        self.assertEqual(len(self.driver.current_station.available_packages), 0)
        self.assertEqual(self.driver.packages_delivered, 1)
        self.assertEqual(self.driver.itinerary, [
            '[6:00]: START work at station A',
            '[6:00]: PICK UP package P1 from station A',
            '[7:00]: DELIVER package P1 to station B'
        ])
    
    def test_clock_print(self):
        self.assertEqual(self.driver.clock_print(), '6:00')

if __name__ == '__main__':
    unittest.main()