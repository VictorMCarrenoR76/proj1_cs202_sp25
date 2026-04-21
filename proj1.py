#Victor Manuel Carreno Rodriguez, Data Structures
import math
from typing import *
from dataclasses import dataclass


@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str

@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

#Task 2:
tokyo_rect = GlobeRect(35.5, 36.0, 139.5, 140.0)
tokyo = Region(tokyo_rect, "Tokyo", "other")
rc1 = RegionCondition(tokyo, 2025, 37000000, 1.2e8)
ny_rect = GlobeRect(40.5, 41.0, -74.3, -73.7)
ny = Region(ny_rect, "New York", "other")
rc2 = RegionCondition(ny, 2025, 20000000, 8.0e7)
ocean_rect = GlobeRect(-10.0, 10.0, -150.0, -120.0)
ocean = Region(ocean_rect, "Pacific Patch", "ocean")
rc3 = RegionCondition(ocean, 2025, 0, 1.0e6)
slo_rect = GlobeRect(35.1, 35.5, -120.9, -120.4)
slo = Region(slo_rect, "San Luis Obispo", "forest")
rc4 = RegionCondition(slo, 2025, 50000, 2.0e5)
region_conditions = [rc1, rc2, rc3, rc4]

#Task 3:
def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate / rc.pop

def area(gr: GlobeRect) -> float:
    R = 6378.1
    phi1 = math.radians(gr.lo_lat)
    phi2 = math.radians(gr.hi_lat)
    lam1 = math.radians(gr.west_long)
    lam2 = math.radians(gr.east_long)
    d_lambda = lam2 - lam1
    if d_lambda < 0:
        d_lambda += 2 * math.pi
    return (R ** 2) * abs(d_lambda) * abs(math.sin(phi2) - math.sin(phi1))

def emissions_per_square_km(rc: RegionCondition) -> float:
    a = area(rc.region.rect)
    if a == 0:
        return 0.0
    return rc.ghg_rate / a

def densest(rc_list: List[RegionCondition]) -> str:
    if len(rc_list) == 1:
        return rc_list[0].region.name
    first = rc_list[0]
    rest_name = densest(rc_list[1:])
    rest = _find_by_name(rc_list[1:], rest_name)
    first_density = first.pop / area(first.region.rect) if area(first.region.rect) != 0 else 0
    rest_density = rest.pop / area(rest.region.rect) if area(rest.region.rect) != 0 else 0
    if first_density >= rest_density:
        return first.region.name
    else:
        return rest_name

def _find_by_name(rc_list: List[RegionCondition], name: str) -> RegionCondition:
    if rc_list[0].region.name == name:
        return rc_list[0]
    return _find_by_name(rc_list[1:], name)

#Task 4:
def _growth_rate(terrain: str) -> float:
    if terrain == "ocean":
        return 0.0001
    elif terrain == "mountains":
        return 0.0005
    elif terrain == "forest":
        return -0.00001
    else:
        return 0.0003

def _project_pop(pop: float, rate: float, years: int) -> float:
    if years == 0:
        return pop
    return _project_pop(pop * (1 + rate), rate, years - 1)

def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    rate = _growth_rate(rc.region.terrain)
    new_pop = _project_pop(rc.pop, rate, years)
    new_ghg = rc.ghg_rate * (new_pop / rc.pop) if rc.pop != 0 else rc.ghg_rate
    return RegionCondition(rc.region,rc.year + years,int(new_pop),new_ghg)
