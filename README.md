# Infection Spread Simulation
This a python program/library that simulates how an infection would spread. The simulation is very crude and probably not useful to draw scientific from.

Credit to my friend Yashwant Konijeti for writing the GUI code.

# How the Simulator works under the hood
First the simulator spawns blobs (the equivalent to people inspired from the YouTube channel Primer) randomly on the map. Each blob has its own home that it might share with others. The simulator will randomly move each blob to a food place (equivalent to a restraunt or work place, this is the name used interanlly in the code) and its home. If the blobs comes close to an infected blob then there is a chance it could get infected.

# How to run the Simulation...
Fist you will have to add all the files (except the main.py as it is just an example) to your project. Other than that you will also need to have pygame and matplotlib added to your project. To run the simulation with a GUI, this is how you do it:
```python
import gui

gui.run(max_infection_distance, infection_probablity, simulation_size)
```

The max_infection_distance parameter determine the furthest distance from which a blob can be infected from. The infection_probability determines the probability of a blob getting infected. The simulation_size parameters determine the number of blobs in the simulation.

But if you want to run the simulation with out the GUI, then this is how you do it:

```python
from Simulation import Simulator

sim = Simulator(homes, food_places, max_infection_distance, infection_probability)

sim.reset_simulation(simulation_size)

prev_time = time.time()

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update time
    game_time = time.time() - prev_time
    prev_time = time.time()
    game_time = round(game_time, 5)
    sim.update_clock(game_time)

    # Update sim
    sim.simulation_cycle()
```
The max_infection_distance, infection_probability and simulation size is the same as the parameters for gui.run(). The homes parameter is a array of pygame Vector2. These locations represent the location of the blob's homes. The food_places parameter is an array of pygame Vector2 which represents the location of the food places (think of them as restruants for the blobs).

If you want to run statistics the gui.run() return a SimulationResults class. 

DISCALIMER: The Simulator class does not contain or return SimulationResults but it does contain all the relevant info.

If you are curious this is all the information the class contains:

```python
class SimulationResults:
    MaxInfectionDistance = 0
    InfectionProbability = 0
    SampleSize = 0

    TotalInfected = []
    TotalInfectedNumber = 0
    TotalInfectedTime = []

    InfectedLocation = []

    InfectedOnWay = []
    InfectedOnWayNumber = 0
    InfectedOnWayTime = []

    InfectedAtPlace = []
    InfectedAtPlaceNumber = 0
    InfectedAtPlaceTime = []
```
All of the variables variables with their suffix as Time is an array on integer of when the next blob got infected.

If you are lazy and just want the statistics then you can you use the following:

```python
import Statistics

Statistics.save_path = "your save path"

#Takes SimuulationResults class as input parameter
run_stats_after_sim(SimulationResults)
```
