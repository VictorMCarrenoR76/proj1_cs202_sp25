#Victor Manuel Carreno Rodriguez
import unittest
from proj1 import *

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(10.0, 20.0, 30.0, 40.0)
        self.region = Region(self.rect, "Testland", "other")
        self.rc = RegionCondition(self.region, 2025, 1000, 5000.0)

    def test_emissions_per_capita(self):
        self.assertAlmostEqual(emissions_per_capita(self.rc), 5.0, places=4)

    def test_emissions_per_capita_zero(self):
        rc = RegionCondition(self.region, 2025, 0, 5000.0)
        self.assertEqual(emissions_per_capita(rc), 0.0)

    def test_area(self):
        self.assertGreater(area(self.rect), 0)

    def test_emissions_per_square_km(self):
        self.assertGreater(emissions_per_square_km(self.rc), 0)

    def test_densest(self):
        rc2 = RegionCondition(self.region, 2025, 2000, 5000.0)
        self.assertEqual(densest([self.rc, rc2]), "Testland")

    def test_project_condition_year(self):
        projected = project_condition(self.rc, 5)
        self.assertEqual(projected.year, 2030)

    def test_project_condition_growth(self):
        projected = project_condition(self.rc, 10)
        self.assertGreater(projected.pop, self.rc.pop)

    def test_project_condition_immutable(self):
        projected = project_condition(self.rc, 5)
        self.assertNotEqual(projected, self.rc)


if __name__ == '__main__':
    unittest.main()
