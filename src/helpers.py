import imp
import playsound
from threading import Thread

# method to print the averages in a nicer format along with the suggested tyre usage
def print_averages(player_car):
    """ This method prints the averages of the car in a nicer format, along with suggested fuel weight, ERS strategy, and tyre stats

    Args:
        player_car (PlayerCar): The car to print the averages for
    """
    strategy_file = open("strategy.txt", "w")
    
    # Write the average fuel consumption
    strategy_file.write(f"Average fuel consumption: {round(player_car.average_fuel_consumption_weight, 2)}kg/lap, Fuel Delta from MFD: ")
    if player_car.average_fuel_consumption_mfd - 1 > 0:
        strategy_file.write(f" +{round(player_car.average_fuel_consumption_mfd - 1, 2)}\n\n")
    else:
        strategy_file.write(f"{round(player_car.average_fuel_consumption_mfd - 1, 2)}\n\n")
    # Write the suggested fuel weight for the race
    strategy_file.write(f"Suggested fuel for the race is {(player_car.average_fuel_consumption_weight * player_car.number_of_race_laps) + 1}Kg including 1Kg extra for margin of error\n")

    # Write the ERS stats
    strategy_file.write(f"Your average ers style was ")
    if player_car.average_ers_deployed - player_car.average_ers_harvested > 0:
        strategy_file.write(f"using {round(player_car.average_ers_deployed - player_car.average_ers_harvested, 2)}Mj of ers a lap or using {round((player_car.average_ers_deployed - player_car.average_ers_harvested)*100/4,2)}% of the battery per lap\n")
        strategy_file.write(f"You can sustain this usage from 100% battery for {round(player_car.average_ers_duration, 2)}laps\n")
        strategy_file.write(f"You should try this for the ERS usage(Assuming max usage 1st lap and keeping about 30% in reserve for defending/attacking):\nWhere F = first, D = Deploy, C = charge\n{get_ers_strat(player_car)}\n\n")

    elif player_car.average_ers_deployed - player_car.average_ers_harvested < 0:
        strategy_file.write(f"harvesting {round(player_car.average_ers_harvested - player_car.average_ers_deployed, 2)}Mj of ers a lap or charging {round((player_car.average_ers_harvested - player_car.average_ers_deployed)*100/4,2)}% per lap\n")
        strategy_file.write(f"Your battery will be fully charged from empty in {round(4.0/(player_car.average_ers_harvested - player_car.average_ers_deployed),2)}laps\n\n")
    else:
        strategy_file.write(f"perfectly balanced as everything should be\n\n")

    # Write the tyre stats and the most worn tyre
    if get_tyre_compound(player_car.tyre_compound) != 'Invalid tyre compound' and get_visual_tyre_compound(
            player_car.tyre_compound_visual) != 'Invalid tyre compound':
        strategy_file.write(f"You completed your laps on the {get_tyre_compound(player_car.tyre_compound)} {get_visual_tyre_compound(player_car.tyre_compound_visual)} \n")
        strategy_file.write(f"Your most worn tyre is the ")
        max_tyre_index = player_car.average_tyre_wear.index(
            max(player_car.average_tyre_wear))
        if max_tyre_index == 0:
            strategy_file.write(f"Rear Left\n")
        elif max_tyre_index == 2:
            strategy_file.write(f"Front Left\n")
        elif max_tyre_index == 1:
            strategy_file.write(f"Rear Right\n")
        elif max_tyre_index == 3:
            strategy_file.write(f"Front Right\n")
    else:
        strategy_file.write(f"Unfortunately your tyre compound was not detected\n")

    # write the average tyre wear with two decimal places
    strategy_file.write(f"Average tyre wear:\n")
    strategy_file.write(f"Rear Left: {round(player_car.average_tyre_wear[0], 2)}% per lap\n")
    strategy_file.write(f"Rear Right: {round(player_car.average_tyre_wear[1], 2)}% per lap\n")
    strategy_file.write(f"Front Left: {round(player_car.average_tyre_wear[2], 2)}% per lap\n")
    strategy_file.write(f"Front Right: {round(player_car.average_tyre_wear[3], 2)}% per lap\n\n")

    # write the average tyre temperatures with two decimal places, along with the min and max temperatures
    strategy_file.write(f"Your tyre temperature information is:\n")
    strategy_file.write(f"Rear Left\nAverage: Surface Temp: {round(player_car.average_tyre_surface_temperature[0], 2)}C Carcass/Inner Temp: {round(player_car.average_tyre_carcass_temperature[0], 2)}C")
    strategy_file.write(f"\nMinimum: Surface Temp: {round(player_car.min_tyre_temps_surface[0], 2)}C Carcass/Inner Temp: {round(player_car.min_tyre_temps_carcass[0], 2)}C")
    strategy_file.write(f"\nMaximum: Surface Temp: {round(player_car.max_tyre_temps_surface[0], 2)}C Carcass/Inner Temp: {round(player_car.max_tyre_temps_carcass[0], 2)}C\n\n")

    strategy_file.write(f"Rear Right\nAverage: Surface Temp: {round(player_car.average_tyre_surface_temperature[1], 2)}C Carcass/Inner Temp: {round(player_car.average_tyre_carcass_temperature[1], 2)}C")
    strategy_file.write(f"\nMinimum: Surface Temp: {round(player_car.min_tyre_temps_surface[1], 2)}C Carcass/Inner Temp: {round(player_car.min_tyre_temps_carcass[1], 2)}C")
    strategy_file.write(f"\nMaximum: Surface Temp: {round(player_car.max_tyre_temps_surface[1], 2)}C Carcass/Inner Temp: {round(player_car.max_tyre_temps_carcass[1], 2)}C\n\n")

    strategy_file.write(f"Front Left\nAverage: Surface Temp: {round(player_car.average_tyre_surface_temperature[2], 2)}C Carcass/Inner Temp: {round(player_car.average_tyre_carcass_temperature[2], 2)}C")
    strategy_file.write(f"\nMinimum: Surface Temp: {round(player_car.min_tyre_temps_surface[2], 2)}C Carcass/Inner Temp: {round(player_car.min_tyre_temps_carcass[2], 2)}C")
    strategy_file.write(f"\nMaximum: Surface Temp: {round(player_car.max_tyre_temps_surface[2], 2)}C Carcass/Inner Temp: {round(player_car.max_tyre_temps_carcass[2], 2)}C\n\n")

    strategy_file.write(f"Front Right\nAverage: Surface Temp: {round(player_car.average_tyre_surface_temperature[3], 2)}C Carcass/Inner Temp: {round(player_car.average_tyre_carcass_temperature[3], 2)}C")
    strategy_file.write(f"\nMinimum: Surface Temp: {round(player_car.min_tyre_temps_surface[3], 2)}C Carcass/Inner Temp: {round(player_car.min_tyre_temps_carcass[3], 2)}C")
    strategy_file.write(f"\nMaximum: Surface Temp: {round(player_car.max_tyre_temps_surface[3], 2)}C Carcass/Inner Temp: {round(player_car.max_tyre_temps_carcass[3], 2)}C\n\n")

    strategy_file.write(f"That's all for now.")
    strategy_file.close()
    print("Find the results in the strategy.txt file")
    import F1Tool.src.main
    F1Tool.src.main.loop = False


def get_tyre_compound(tyre_compound):
    """ Returns the specfic tyre compound as a string

    Args:
        tyre_compound (int): The tyre compound as an integer

    Returns:
        str: based on input, returns the tyre compound, in = out: 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1, 7 = Inters, 8 = Wet
    """
    if tyre_compound != None or tyre_compound != 0:
        # return the number of the tyre compound 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1, 7 = Inters, 8 = Wet
        if tyre_compound == 16:
            return 'C5'
        elif tyre_compound == 17:
            return 'C4'
        elif tyre_compound == 18:
            return 'C3'
        elif tyre_compound == 19:
            return 'C2'
        elif tyre_compound == 20:
            return 'C1'
        elif tyre_compound == 7:
            return 'Inters'
        elif tyre_compound == 8:
            return 'Wet'
    else:
        return "Invalid tyre compound"


def get_visual_tyre_compound(tyre_compound_visual):
    """ Returns the visual tyre compound as a string

    Args:
        tyre_compound_visual (int): The tyre compound as an integer

    Returns:
        string: based on input, returns the tyre compound, in = out: 16 = soft, 17 = medium, 18 = hard, 7 = inters, 8 = wet
    """
    if tyre_compound_visual != None or tyre_compound_visual != 0:
        # return the number of the tyre compound 16 = soft, 17 = medium, 18 = hard, 7 = inters, 8 = wet
        if tyre_compound_visual == 16:
            return 'soft'
        elif tyre_compound_visual == 17:
            return 'medium'
        elif tyre_compound_visual == 18:
            return 'hard'
        elif tyre_compound_visual == 7:
            return 'inters'
        elif tyre_compound_visual == 8:
            return 'wet'
    else:
        return "Invalid tyre compound"

def get_ers_strat(player_car):
    """ Returns the suggested ERS strategy as a string

    Args:
        player_car (PlayerCar): The player car object

    Returns:
        str: The ERS strategy as a string, where F = First lap, D = Deploy, C = Charge
    """
    ret = "F"
    # full battery at the start, 4Mj
    current_battery = 4.0
    
    for i in range(1,player_car.number_of_race_laps):
        
        # Max usage first lap, with only 80% harvest because of traffic/standing start
        if i == 1:
            current_battery -= 4.0 - (player_car.average_ers_harvested * 0.8)
        # if battery is enough to last till the last lap, just use it
        elif i > player_car.number_of_race_laps - current_battery/(player_car.average_ers_deployed - player_car.average_ers_harvested):
            ret+= "D"
        # if battery over 10%, then deploy
        elif current_battery - (player_car.average_ers_deployed - player_car.average_ers_harvested) > 4.0*0.1:
            current_battery -= player_car.average_ers_deployed - player_car.average_ers_harvested
            ret+= "D"
        # if battery is less than 10%, then charge by deploying very little(turn off ERS for most of the time, with some deploy at critical sections),
        # along with harder braking for more MGUK Harvest
        else:
            ret += "C"
            current_battery += min(4.0, player_car.average_ers_harvested*1.2 - (player_car.average_ers_deployed*0.2))
    return ret

# https://stackoverflow.com/a/69220119
def play_audio(audiopath, is_quick=False):
    """
    Play sound file in a separate thread
    only plays if is_quick is False
    (don't block current thread)
    """
    if not is_quick:
        def play_thread_function():
            playsound.playsound(audiopath)

        play_thread = Thread(target=play_thread_function)
        play_thread.start()
