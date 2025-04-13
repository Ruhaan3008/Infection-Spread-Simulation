import pygame

from Simulation import Simulator
from blob import BlobState
import Statistics

import time

# Set up the game window
screen_width = 1000
screen_height = 770


# Define colors
healthy_color = (67, 236, 99)
infected_color = (248, 128, 99)
recovered_color = (30, 30, 30)

# Define blob representation
blob_radius = 8

place_width = 40
place_height = 20

render_time = []

# Define locations for places
food_places = [(336, 619), (660, 367), (825, 569), (372, 250),
               (617, 708), (171, 29), (706, 33), (57, 299), (908, 260)]
homes = [(563, 159), (206, 159), (848, 159), (162, 364),
         (410, 397), (898, 400), (104, 639), (603, 518), (908, 721)]


def draw_blobs(sim, screen):
    for blob in sim.blobs:
        color = healthy_color if blob.HealthStatus == BlobState.Healthy else infected_color
        if blob.HealthStatus == BlobState.Recovered:
            color = recovered_color
        pygame.draw.circle(screen, (0, 0, 0), blob.Location, blob_radius + 2)
        pygame.draw.circle(screen, color, blob.Location, blob_radius)


def draw_places(sim, screen):
    for place in sim.HomeLocations:
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(place[0] - place_width, place[1] - place_height,
                                     (place_width * 2) + 2, (place_height * 2) + 2))
        pygame.draw.rect(screen, (31, 166, 72), pygame.Rect(place[0] - (place_width - 2),
                                                            place[1] - (place_height - 2),
                                                            (place_width * 2) - 2, (place_height * 2) - 2))

    for place in sim.FoodLocations:
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(place[0] - place_width, place[1] - place_height,
                                     (place_width * 2) + 2, (place_height * 2) + 2))
        pygame.draw.rect(screen, (255, 231, 75), pygame.Rect(place[0] - (place_width - 2),
                                                             place[1] - (place_height - 2),
                                                             (place_width * 2) - 2, (place_height * 2) - 2))


def run(max_infection_dist, infection_probability, simulation_size, infection_time = 60):
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Blob Simulation')

    sim = Simulator(homes, food_places, max_infection_dist, infection_probability)

    sim.reset_simulation(simulation_size)
    sim.InfectionTime = infection_time

    prev_time = time.time()

    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update time
        game_time = time.time() - prev_time
        prev_time = time.time()
        game_time = round(game_time, 5)

        render_time.append(game_time)

        sim.update_clock()

        # Update sim
        sim.simulation_cycle()

        # Clear the screen
        screen.fill((255, 255, 255))  # Set background color to white

        # Draw blobs
        draw_blobs(sim, screen)

        # Draw food places, workplaces, and leisure areas
        draw_places(sim, screen)

        # Update the screen
        pygame.display.flip()

        clock.tick(60)

    # Quit Pygame
    pygame.quit()

    avg_render_time = sum(render_time)/len(render_time)
    print("Average Render Time: " + str(avg_render_time))

    sam = simulation_size
    mid = sim.MaxInfectionDistance
    ip = sim.InfectionProbability

    ti = sim.TotalInfected
    tin = sim.TotalInfectedNumber
    tit = sim.TotalInfectedTime

    io = sim.InfectedOnWay
    ion = sim.InfectedOnWayNumber
    iot = sim.InfectedOnWayTime

    ia = sim.InfectedAtPlace
    ian = sim.InfectedAtPlaceNumber
    iat = sim.InfectedAtPlaceTime

    il = sim.InfectedLocation

    stats = Statistics.SimulationResults(sam, mid, ip, ti, tin, tit, io, ion, iot, ia, ian, iat, il)
    return stats
