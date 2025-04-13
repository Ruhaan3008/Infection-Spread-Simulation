import random
from pygame import Vector2
from enum import Enum

class BlobState(Enum):
    Healthy = 0
    Infected = 1
    Recovered = 2

class Blob:
    HealthStatus = BlobState.Healthy

    RecoveryTime = 0

    Location = Vector2(0, 0)
    HomeLocation: Vector2 = None
    WorkLocation: Vector2 = None

    ActionStartTime = 0
    ActionEndTime = 0

    InAction = False
    NextAction = 0

    TargetLocation = Vector2(770, 770)
    AtLocation = False
    RestTimer = 0

    MoveDistance = 20

    def __init__(self, is_infected, loc, sim):
        self.Location = loc
        self.Sim = sim
        self.TargetLocation = loc

        if is_infected:
            self.HealthStatus = BlobState.Infected
            return
        self.HealthStatus = BlobState.Healthy

    def blob_start_action(self, clock, time):
        self.ActionStartTime = clock
        self.ActionEndTime = (clock + time)
        self.AtLocation = True
        self.InAction = True

    def if_at_location_tasks_and_checks(self):
        if self.HealthStatus == BlobState.Infected:
            self.RecoveryTime -= (random.randint(1, 3))
            if self.RecoveryTime <= 0:
                self.HealthStatus = BlobState.Recovered
        if self.Location.distance_to(self.TargetLocation) < 0.1:
            self.RestTimer -= (random.randint(2, 5))
            if self.RestTimer <= 0:
                self.set_new_target()
        else:
            self.move()

    def move(self):
        self.Location = Vector2.move_towards(self.Location, self.TargetLocation, self.MoveDistance)
        if self.Location == self.TargetLocation:
            self.RestTimer = 40

    def set_home(self):
        self.HomeLocation = self.Sim.HomeLocations[(random.randint(0, 100) % len(self.Sim.HomeLocations))]

    def set_new_target(self):

        if self.NextAction % 2 == 1:
            self.TargetLocation = self.HomeLocation
            self.NextAction += 1
            return
        self.TargetLocation = random.choice(self.Sim.FoodLocations)
        self.NextAction += 1
        return


    def blob_cycle(self):
        self.if_at_location_tasks_and_checks()
