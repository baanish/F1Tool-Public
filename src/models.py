class PlayerCar:
    # These store the data for the car for every tick
    tyre_wear = []
    fuel_weight = []
    fuel_mfd = []
    ers_current = []
    ers_deployed = []
    ers_harvested = []
    tyre_surface_temperature = []
    tyre_carcass_temperature = []
    
    # These are the variables that are used to store the data for the car every time a lap is completed
    tyre_wear_per_lap = []
    fuel_weight_per_lap = []
    fuel_mfd_per_lap = []
    tyre_surface_temperature_per_lap = []
    tyre_carcass_temperature_per_lap = []
    ers_current_per_lap = []
    ers_deployed_per_lap = []
    ers_harvested_per_lap = []
    
    # Variables that are used to store the data about laps
    completed_laps = 0
    number_of_laps = 5
    number_of_race_laps = 0
    
    # averages
    average_fuel_consumption_weight = 0.0
    average_fuel_consumption_mfd = 0.0
    average_tyre_wear = []
    average_tyre_surface_temperature = []
    average_tyre_carcass_temperature = []
    average_ers_duration = 0.0
    average_ers_deployed = 0.0
    average_ers_harvested = 0.0
    
    # tyre data
    tyre_compound = 0
    tyre_compound_visual = 0
    min_tyre_temps_surface = [1000,1000,1000,1000]
    max_tyre_temps_surface = [0,0,0,0]
    min_tyre_temps_carcass = [1000,1000,1000,1000]
    max_tyre_temps_carcass = [0,0,0,0]

    # constructor for the player car
    def __init__(self, start_tyre_wear, start_fuel_weight, start_fuel_mfd, number_of_laps, number_of_race_laps,
                 tyre_compound, tyre_compound_visual):
        """ This class stores the data for the player car. It also performs the basic updates the data per lap and calculates the averages

        Args:
            start_tyre_wear (float[]): An array of the starting tyre wear for each tyre ordered RL, RR, FL, FR
            start_fuel_weight (float): The weight of the fuel in the car
            start_fuel_mfd (float): The number of laps of fuel based on the MFD
            number_of_laps (int): Number of laps to calculate the averages for
            number_of_race_laps (int): Number of laps in the race
            tyre_compound (int): The tyre compound number
            tyre_compound_visual (int): The tyre compound name
        """
        self.number_of_laps = number_of_laps
        self.tyre_wear_per_lap.append(start_tyre_wear)
        self.fuel_weight_per_lap.append(start_fuel_weight)
        self.fuel_mfd_per_lap.append(start_fuel_mfd)
        self.number_of_race_laps = number_of_race_laps
        self.tyre_compound = tyre_compound
        self.tyre_compound_visual = tyre_compound_visual

    def lap_completed(self):
        """
        This function is called when a lap is completed. It updates the data for the lap by populating the per lap arrays
        it also calculates the averages if the number of laps is reached. It then calls the print_averages function to print the averages
        """
        
        # increment the number of completed laps
        self.completed_laps += 1
        
        # update the per lap arrays
        self.fuel_weight_per_lap.append(
            self.fuel_weight[len(self.fuel_weight) - 1])
        self.fuel_mfd_per_lap.append(self.fuel_mfd[len(self.fuel_mfd) - 1])
        self.tyre_wear_per_lap.append(self.tyre_wear[len(self.tyre_wear) - 1])
        self.tyre_surface_temperature_per_lap.append(self.tyre_surface_temperature[len(self.tyre_surface_temperature) - 1])
        self.tyre_carcass_temperature_per_lap.append(self.tyre_carcass_temperature[len(self.tyre_carcass_temperature) - 1])
        self.ers_current_per_lap.append(self.ers_current[len(self.ers_current) - 1])
        self.ers_deployed_per_lap.append(self.ers_deployed[len(self.ers_deployed) - 1])
        self.ers_harvested_per_lap.append(self.ers_harvested[len(self.ers_harvested) - 1])
        
        # calculate averages if number of laps is reached
        if self.completed_laps == self.number_of_laps:
            
            rl_average_tyre_wear, rr_average_tyre_wear, fl_average_tyre_wear, fr_average_tyre_wear = 0, 0, 0, 0
            
            # sum up the averages for fuel and tyres
            for i in range(self.number_of_laps):
                
                self.average_fuel_consumption_weight += (
                        self.fuel_weight_per_lap[i] - self.fuel_weight_per_lap[i + 1])
                self.average_fuel_consumption_mfd += (
                        self.fuel_mfd_per_lap[i] - self.fuel_mfd_per_lap[i + 1])
                
                rl_average_tyre_wear += self.tyre_wear_per_lap[i +
                                                               1][0] - self.tyre_wear_per_lap[i][0]
                rr_average_tyre_wear += self.tyre_wear_per_lap[i +
                                                               1][1] - self.tyre_wear_per_lap[i][1]
                fl_average_tyre_wear += self.tyre_wear_per_lap[i +
                                                               1][2] - self.tyre_wear_per_lap[i][2]
                fr_average_tyre_wear += self.tyre_wear_per_lap[i +
                                                               1][3] - self.tyre_wear_per_lap[i][3]

            # Calculate the averages for fuel and tyres, just a simple sum and divide by the number of laps
            self.average_fuel_consumption_weight = round(
                self.average_fuel_consumption_weight / (len(self.fuel_weight_per_lap) - 1), 2)
            self.average_fuel_consumption_mfd = round(
                self.average_fuel_consumption_mfd / (len(self.fuel_mfd_per_lap) - 1), 2)
            fr_average_tyre_wear = fr_average_tyre_wear / \
                                   (len(self.tyre_wear_per_lap) - 1)
            fl_average_tyre_wear = fl_average_tyre_wear / \
                                   (len(self.tyre_wear_per_lap) - 1)
            rr_average_tyre_wear = rr_average_tyre_wear / \
                                   (len(self.tyre_wear_per_lap) - 1)
            rl_average_tyre_wear = rl_average_tyre_wear / \
                                   (len(self.tyre_wear_per_lap) - 1)
            self.average_tyre_wear = [rl_average_tyre_wear, rr_average_tyre_wear, fl_average_tyre_wear,
                                      fr_average_tyre_wear]
            
            rl_average_tyre_temp_surface, rr_average_tyre_temp_surface, fl_average_tyre_temp_surface, fr_average_tyre_temp_surface = 0, 0, 0, 0
            rl_average_tyre_temp_carcass, rr_average_tyre_temp_carcass, fl_average_tyre_temp_carcass, fr_average_tyre_temp_carcass = 0, 0, 0, 0
            
            # sum up the tyre temperatures
            for i in range(len(self.tyre_surface_temperature)):
                rl_average_tyre_temp_surface += self.tyre_surface_temperature[i][0]
                rr_average_tyre_temp_surface += self.tyre_surface_temperature[i][1]
                fl_average_tyre_temp_surface += self.tyre_surface_temperature[i][2]
                fr_average_tyre_temp_surface += self.tyre_surface_temperature[i][3]
                
            for i in range(len(self.tyre_carcass_temperature)):
                rl_average_tyre_temp_carcass += self.tyre_carcass_temperature[i][0]
                rr_average_tyre_temp_carcass += self.tyre_carcass_temperature[i][1]
                fl_average_tyre_temp_carcass += self.tyre_carcass_temperature[i][2]
                fr_average_tyre_temp_carcass += self.tyre_carcass_temperature[i][3]

            # calculate the averages for the tyre temperatures this is a sum and divide by length of the array
            rl_average_tyre_temp_surface = rl_average_tyre_temp_surface/len(self.tyre_surface_temperature)
            rr_average_tyre_temp_surface = rr_average_tyre_temp_surface/len(self.tyre_surface_temperature)
            fl_average_tyre_temp_surface = fl_average_tyre_temp_surface/len(self.tyre_surface_temperature)
            fr_average_tyre_temp_surface = fr_average_tyre_temp_surface/len(self.tyre_surface_temperature)
            self.average_tyre_surface_temperature = [rl_average_tyre_temp_surface, rr_average_tyre_temp_surface, fl_average_tyre_temp_surface, fr_average_tyre_temp_surface]

            rl_average_tyre_temp_carcass = rl_average_tyre_temp_carcass/len(self.tyre_carcass_temperature)
            rr_average_tyre_temp_carcass = rr_average_tyre_temp_carcass/len(self.tyre_carcass_temperature)
            fl_average_tyre_temp_carcass = fl_average_tyre_temp_carcass/len(self.tyre_carcass_temperature)
            fr_average_tyre_temp_carcass = fr_average_tyre_temp_carcass/len(self.tyre_carcass_temperature)
            self.average_tyre_carcass_temperature = [rl_average_tyre_temp_carcass, rr_average_tyre_temp_carcass, fl_average_tyre_temp_carcass, fr_average_tyre_temp_carcass]

            # calculate the average ERS deploy and harvest
            self.average_ers_deployed = round(sum(self.ers_deployed_per_lap) / (len(self.ers_deployed_per_lap)), 2)
            self.average_ers_harvested = round(sum(self.ers_harvested_per_lap) / (len(self.ers_harvested_per_lap)), 2)

            # If the deploy is more than the harvest, then calculate how many laps the ERS will last
            if self.average_ers_deployed - self.average_ers_harvested > 0:
                self.average_ers_duration = 4.0/(self.average_ers_deployed - self.average_ers_harvested)
            else:
                self.average_ers_duration = 0.0
            
            # call the helper function to print the averages
            from helpers import print_averages
            print_averages(self)

    def tick_fuel_and_ers(self, fuel_weight, fuel_mfd, ers_current, ers_deployed, ers_harvested):
        """ This function is called to update the fuel and ERS status

        Args:
            fuel_weight (float): The current fuel weight(kg)
            fuel_mfd (float): The current fuel according to the MFD(laps)
            ers_current (float): The current ERS level(joules), This will be converted to MegaJoules
            ers_deployed (float): The ERS deployed this lap(joules), This will be converted to MegaJoules
            ers_harvested (float): The ERS harvested this lap(joules), This will be converted to MegaJoules
        """
        self.fuel_weight.append(fuel_weight)
        self.fuel_mfd.append(fuel_mfd)
        #convert to Mj from j
        self.ers_current.append(ers_current/1000000)
        self.ers_deployed.append(ers_deployed/1000000)
        self.ers_harvested.append(ers_harvested/1000000)

    def tick_tyre(self, tyre_wear):
        """ This function is called to update the tyre wear

        Args:
            tyre_wear (float[]): The tyre wear for each tyre(%), order is RL, RR, FL, FR
        """
        self.tyre_wear.append(tyre_wear)

    def tick_temps(self, tyre_surface_temperature, tyre_carcass_temperature):
        """ This function is called to update the tyre temperatures

        Args:
            tyre_surface_temperature (float[]): The tyre surface temperature for each tyre(C), order is RL, RR, FL, FR
            tyre_carcass_temperature (float[]): The tyre carcass(core/inner layer) temperature for each tyre(C), order is RL, RR, FL, FR
        """
        self.tyre_surface_temperature.append(tyre_surface_temperature)
        self.tyre_carcass_temperature.append(tyre_carcass_temperature)
        #update min and max tyre temps for surface and carcass
        if self.min_tyre_temps_carcass == None:
            self.min_tyre_temps_carcass = tyre_carcass_temperature
            self.max_tyre_temps_carcass = tyre_carcass_temperature
            self.min_tyre_temps_surface = tyre_surface_temperature
            self.max_tyre_temps_surface = tyre_surface_temperature
        for i in range(4):
            self.min_tyre_temps_carcass[i] = min(self.min_tyre_temps_carcass[i], tyre_carcass_temperature[i])
            self.max_tyre_temps_carcass[i] = max(self.max_tyre_temps_carcass[i], tyre_carcass_temperature[i])
            self.min_tyre_temps_surface[i] = min(self.min_tyre_temps_surface[i], tyre_surface_temperature[i])
            self.max_tyre_temps_surface[i] = max(self.max_tyre_temps_surface[i], tyre_surface_temperature[i])