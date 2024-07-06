import matplotlib.pyplot as plt
import numpy as np
import pandas as excel

save_path = "D:/SimRes"

def plot(x_points, y_points, title):
    plt.clf()
    plt.plot(x_points, y_points)
    plt.savefig(save_path + "/" + title+".png")
    plt.title = title
    plt.show()


def plot_heat_map(loc_arr, title):
    map_arr = np.zeros(shape=(8, 10))

    for loc in loc_arr:
        x = round(loc.x / 100)
        y = round(loc.y / 100)
        map_arr[y - 1][x - 1] += 1

    plt.imshow(map_arr)

    plt.savefig(save_path + "/" + title+".png")

    plt.show()
    pass


def plot_heat_map_high_resolution(loc_arr, name):
    map_arr = np.zeros(shape=(77, 100))
    plt.title = name
    for loc in loc_arr:
        x = round(loc.x / 10)
        y = round(loc.y / 10)
        map_arr[y - 1][x - 1] += 1
        if map_arr[y - 1][x - 1] > 1000:
            map_arr[y - 1][x - 1] = 1000

    plt.imshow(map_arr)

    plt.savefig(save_path + "/" + "Simulation_Graphs/Heat_Maps/"+name)

    plt.show()
    pass


def export_to_excel(total, total_time, on_way, on_way_time, at_home, at_home_time):
    total_array = [["Time", "Total"]]
    on_way_array = [["Time", "Total"]]
    at_home_array = [["Time", "Total"]]

    for i in range(len(total)):
        total_array.append([total_time[i], total[i]])

    for i in range(len(on_way)):
        on_way_array.append([on_way_time[i], on_way[i]])

    for i in range(len(at_home)):
        at_home_array.append([at_home_time[i], at_home[i]])

    df = excel.DataFrame(total_array)
    df2 = excel.DataFrame(on_way_array)
    df3 = excel.DataFrame(at_home_array)

    # df.to_excel(excel_writer="C:/Users/ruhaa/Desktop/test.xlsx")
    with excel.ExcelWriter(save_path + "/" + "Simulation Results.xlsx") as writer:
        # use to_excel function and specify the sheet_name and index
        # to store the dataframe in specified sheet
        df.to_excel(writer, sheet_name="Total Infected", index=False)
        df2.to_excel(writer, sheet_name="Total Infected On Way", index=False)
        df3.to_excel(writer, sheet_name="Total Infected At Home", index=False)


def run_stats_after_sim(sim_results):
    plot(sim_results.TotalInfectedTime, sim_results.TotalInfected, "Total Infected")
    plot(sim_results.InfectedOnWayTime, sim_results.InfectedOnWay, "Blobs Infected on the way")
    plot(sim_results.InfectedAtPlaceTime, sim_results.InfectedAtPlace, "Blobs Infected at Homes")
    export_to_excel(sim_results.TotalInfected, sim_results.TotalInfectedTime,
                    sim_results.InfectedOnWay, sim_results.InfectedOnWayTime,
                    sim_results.InfectedAtPlace, sim_results.InfectedAtPlaceTime)
    plot_heat_map(sim_results.InfectedLocation, "Heat Map")

    print(str(sim_results.TotalInfectedNumber) + " blobs were infected.")
    print(str(sim_results.InfectedAtPlaceNumber) + " blobs were infected while they were at home or while eating.")
    print(str(sim_results.InfectedOnWayNumber) + " blobs were infected while travelling.")


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

    def __init__(self, sam, mid, ip, ti, tin, tit, io, ion, iot, ia, ian, iat, il):
        self.SampleSize = sam
        self.MaxInfectionDistance = mid
        self.InfectionProbability = ip

        self.TotalInfected = ti
        self.TotalInfectedNumber = tin
        self.TotalInfectedTime = tit

        self.InfectedOnWay = io
        self.InfectedOnWayNumber = ion
        self.InfectedOnWayTime = iot

        self.InfectedAtPlace = ia
        self.InfectedAtPlaceNumber = ian
        self.InfectedAtPlaceTime = iat

        self.InfectedLocation = il

