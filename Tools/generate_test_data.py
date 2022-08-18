import json
from os.path import exists

from telemetry_f1_2021.listener import TelemetryListener

# open test_data.txt in write mode
output_file = open("test_data.json", "w")
output_file.write("[\n")

listener = TelemetryListener(
    port=20777, host="127.0.0.1")

print("Waiting for data...")
printed_collecting_data = False
is_tracking = False
while True:
    data = str(listener.get())
    if not printed_collecting_data:
        print("Collecting data...")
        printed_collecting_data = True
    output_file.write(data + ",\n")
    if data.__contains__("m_lap_data"):
        data_json = json.loads(data)

        # the player json is at the m_player_car_index from the packet header
        player_json = data_json.get("m_lap_data")[data_json.get("m_header").get("m_player_car_index")]

        # status = 1 is on hotlap
        if player_json.get("m_driver_status") == 1:
            if not is_tracking:
                is_tracking = True
                current_lap = player_json.get("m_current_lap_num")
        if is_tracking and player_json.get("m_current_lap_num") > current_lap:
            print("lap completed")
            current_lap = player_json.get("m_current_lap_num")
            if current_lap == 4:
                output_file.write("]")
                output_file.close()
                exit(0)
