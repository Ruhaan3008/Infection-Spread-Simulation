import random

from blob import Blob
from itertools import combinations
from pygame import Vector2


class Simulator:
    blobs = []
    HomeLocations = []
    FoodLocations = []

    MaxInfectionDistance = 20
    InfectionProbability = 0

    # time in hours, 1 = one hour, 24 = one day (seconds per hours)
    clock = 0
    rawTime = 0
    SimulationSpeed = 0

    TotalInfectedNumber = 0
    TotalInfected = []
    TotalInfectedTime = []

    InfectedLocation = []

    InfectedOnWay = [0]
    InfectedOnWayNumber = 0
    InfectedOnWayTime = [0]

    InfectedAtPlace = [0]
    InfectedAtPlaceNumber = 0
    InfectedAtPlaceTime = [0]

    def __init__(self, homes, foods, max_infection_dist, infection_probability):
        self.HomeLocations = homes
        self.FoodLocations = foods
        self.MaxInfectionDistance = max_infection_dist
        self.InfectionProbability = 100 - infection_probability

        # graphs and shit
        self.add_total_infected_stats()
        pass

    def update_clock(self, time_in_milliseconds):
        self.clock += time_in_milliseconds
        # self.clock = self.rawTime % self.SimulationSpeed

    def reset_simulation(self, size):
        self.blobs = []
        for i in range(size):
            x = random.randint(0, 1000)
            y = random.randint(0, 770)

            self.blobs.append(Blob(False, Vector2(x, y), self))
            self.blobs[i].set_home()

        x = random.randint(0, 1000)
        y = random.randint(0, 770)

        self.blobs.append(Blob(True, Vector2(x, y), self))
        self.blobs[size].set_home()

    def spread_infection(self):
        arr_len = len(self.blobs)
        for blob, other_blob in combinations(self.blobs, 2):

            if blob.IsInfected == other_blob.IsInfected:
                continue
            
            if blob.IsInfected:
                blob, other_blob = other_blob, blob

            dist_btw_blobs = Vector2.distance_to(blob.Location, other_blob.Location)
            are_blobs_in_range =  dist_btw_blobs <= self.MaxInfectionDistance
            if not are_blobs_in_range:
                continue

            get_infected = random.randint(0, 100) > self.InfectionProbability
            if not get_infected:
                continue
        
            blob.IsInfected = True

            dist_to_target = Vector2.distance_to(blob.Location, blob.TargetLocation)

            self.add_total_infected_stats()
            self.add_infect_on_way_stats(dist_to_target)
            self.add_infect_at_place_stats(dist_to_target)

            self.InfectedLocation.append(blob.Location)

    def add_total_infected_stats(self):
        self.TotalInfectedNumber += 1
        self.TotalInfected.append(self.TotalInfectedNumber)
        self.TotalInfectedTime.append(self.clock)

    def add_infect_on_way_stats(self, dist):
        if dist > self.MaxInfectionDistance:
            self.InfectedOnWayNumber += 1
            self.InfectedOnWay.append(self.InfectedOnWayNumber)
            self.InfectedOnWayTime.append(self.clock)

    def add_infect_at_place_stats(self, dist):
        if dist < self.MaxInfectionDistance:
            self.InfectedAtPlaceNumber += 1
            self.InfectedAtPlace.append(self.InfectedAtPlaceNumber)
            self.InfectedAtPlaceTime.append(self.clock)

    def simulation_cycle(self):
        i = -1
        for blob in self.blobs:
            blob.blob_cycle()
            i += 1
            self.blobs[i] = blob
        self.spread_infection()
