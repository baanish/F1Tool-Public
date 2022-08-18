import json
from os.path import exists
from time import sleep

from telemetry_f1_2021.listener import TelemetryListener

import F1Tool.src.models as models
import cProfile,sys

from F1Tool.src.helpers import play_audio

setup_needed = False

# Load a blank config, populated from file or user input
config = json.loads("{}")
if exists('config.json'):
    # open config file
    config_file = open("config.json", "r").read()

    # check if config file is a valid json file and if config file is valid, load it
    try:
        config = json.loads(config_file)
    except IOError:
        print("Config file is not a valid json file")
        print("Starting setup")
        setup_needed = True
else:
    print("No Config Found")
    print("Starting setup")
    setup_needed = True

if setup_needed:
    config["version"] = 1.1
    config["udp_ip"] = input("Enter UDP IP: ")
    config["udp_port"] = input("Enter UDP Port: ")
    config["num_laps"] = input("Enter Number Of Laps: ")
    # save config file
    config_file = open("config.json", "w")
    config_file.write(json.dumps(config, sort_keys=True, indent=4))

# Listen to the UDP ip and port using the telemetry_f1_2021 package
listener = TelemetryListener(
    port=int(config["udp_port"]), host=config["udp_ip"])

# File to save the packet data to for debugging
# packets_json = open("packets.json", "a+")

# tracks the current lap
current_lap = 0
goal_laps = int(config["num_laps"])
player_car = None

# the status at the start of the first lap
start_tyre_wear = None
start_fuel = None
start_fuel_mfd = None

# used to enable the tracking when player ends outlap
is_tracking = False

# Number of racelaps used to calculate the fuel and ERS strategy
number_of_race_laps = int(input("Enter Number of race laps :"))
tyre_compound = 0
tyre_compound_visual = 0
printed_on_outlap = False
loop = True



def listen_to_udp(test=False,real_time=False):
    global is_tracking, current_lap, printed_on_outlap, start_fuel, start_fuel_mfd, tyre_compound, tyre_compound_visual, start_tyre_wear, player_car
    if test:
        from time import perf_counter
        test_data = {}
        test_data_index = 0
        start = perf_counter()
        print("Reading test data")
        data_load_overhead = perf_counter()
        test_data = json.loads(open("test_data.json", "r").read())
        testing_overhead = perf_counter() - data_load_overhead
        
    while loop:
        # get the packet from the listener and decode it using the telemetry_f1_2021 package, if testing bypass the listener
        if not test and not real_time:
            data = listener.get()
        else:
            overhead_start = perf_counter()
            data = test_data[test_data_index]
            test_data_index += 1
            testing_overhead += perf_counter() - overhead_start

            if real_time:
                sleep(0.001)
        # if the packet has lap data, use it to update the current lap information
        if "m_lap_data" in data:
            
            # the player json is at the m_player_car_index from the packet header
            player_json = data.get("m_lap_data")[data.get(
                "m_header").get("m_player_car_index")]
            
            # status = 1 is on hotlap, so we can start tracking if not already tracking, and update the current lap if the lap number is greater than current_lap
            if player_json.get("m_driver_status") == 1:
                if not is_tracking:
                    is_tracking = True
                    current_lap = player_json.get("m_current_lap_num")
                if is_tracking and player_json.get("m_current_lap_num") > current_lap:
                    print("lap completed")
                    player_car.lap_completed()
                    current_lap = player_json.get("m_current_lap_num")
                    
            # status = 3 is on outlap
            if player_json.get("m_driver_status") == 3 and not printed_on_outlap:
                print("out lap")
                play_audio(".\\sounds\\outlap.mp3")
                printed_on_outlap = True

        # if the packet has car status data, use it to update the player car's fuel, ERS. It is also used to set the tyre compound
        if ("m_car_status_data" in data):
            # packets_json.write(str(data_json.get("m_car_status_data")[data_json.get("m_header").get("m_player_car_index")]).replace("\'", "\"") + ',\n')
            player_json = data.get("m_car_status_data")[
                data.get("m_header").get("m_player_car_index")]

            if is_tracking and start_fuel is None and start_fuel_mfd is None:
                print("starting first lap")
                play_audio(".\\sounds\\first_lap.mp3")
                start_fuel = player_json.get("m_fuel_in_tank")
                start_fuel_mfd = player_json.get("m_fuel_remaining_laps")
                tyre_compound = player_json.get("m_actual_tyre_compound")
                tyre_compound_visual = player_json.get("m_visual_tyre_compound")
            if is_tracking and player_car is not None:
                player_car.tick_fuel_and_ers(player_json.get(
                    "m_fuel_in_tank"), player_json.get("m_fuel_remaining_laps"), player_json.get("m_ers_store_energy"),
                    player_json.get("m_ers_deployed_this_lap"),
                    player_json.get("m_ers_harvested_this_lap_mguk") + player_json.get("m_ers_harvested_this_lap_mguh"))

        # if the packet has damage data, use it to update the player car's tyre wear
        if ('m_car_damage_data' in data):
            # packets_json.write(str(data_json.get("m_car_damage_data")[data_json.get("m_header").get("m_player_car_index")]).replace("\'", "\"") + ',\n')
            player_json = data.get("m_car_damage_data")[
                data.get("m_header").get("m_player_car_index")]
            # print("RL Wear: " + str(player_json.get("m_tyres_wear")[0]) + "% RR Wear" + str(player_json.get("m_tyres_wear")[1]) + "% FL Wear" + str(player_json.get("m_tyres_wear")[2]) + "% FR Wear" + str(player_json.get("m_tyres_wear")[3]) + "%")
            if is_tracking and start_tyre_wear == None:
                start_tyre_wear = player_json.get("m_tyres_wear")
            if is_tracking and player_car is not None:
                player_car.tick_tyre(player_json.get("m_tyres_wear"))

        # if the packet has telemetry data, use it to update the player car's tyre temperature
        if ('m_car_telemetry_data' in data):
            player_json = data.get("m_car_telemetry_data")[
                data.get("m_header").get("m_player_car_index")]
            if is_tracking and player_car is not None:
                player_car.tick_temps(
                    player_json.get('m_tyres_surface_temperature'), player_json.get('m_tyres_inner_temperature'))

        # if the start values are set, create the player car
        if player_car is None and start_fuel is not None and start_fuel_mfd is not None and start_tyre_wear is not None:
            player_car = models.PlayerCar(start_tyre_wear, start_fuel, start_fuel_mfd, int(config["num_laps"]),
                                          number_of_race_laps, tyre_compound, tyre_compound_visual)
    if test:
        method_time_taken = perf_counter() - start
        print(f"Code ran in {method_time_taken - testing_overhead} seconds with a testing overhead of: {testing_overhead} seconds")
        print(f"Loop duration is: {loop_duration} seconds")
        print(f"Loop count is: {loop_count}")
        print(f"Average loop is: {loop_duration/loop_count} seconds")
        

# if in profile mode run for profiling
if len(sys.argv) > 1 and sys.argv[1] == "profile":
    print("profiling")
    cProfile.run(listen_to_udp())