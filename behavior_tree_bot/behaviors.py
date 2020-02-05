import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_highest_priority_planet(state):
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    highest_priority=0
    min_source_planet=None
    min_dst_planet=None    
    max_growth_rate=0
    required_ships_final =0
    for my_planet in state.my_planets():
        for target_planet in enemy_planets:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            priority=2*target_planet.growth_rate/state.distance(my_planet.ID, target_planet.ID)
            if(my_planet.num_ships>required_ships):
                if (priority>highest_priority)  or (priority==highest_priority and required_ships<required_ships_final):
                    min_source_planet=my_planet
                    min_dst_planet=target_planet
                    required_ships_final =required_ships
                    highest_priority=priority

    if not min_source_planet or not min_dst_planet:
        return False
    else:
        
        return issue_order(state,min_source_planet.ID, min_dst_planet.ID, required_ships_final)
        

def spread_to_highest_priority_all_planet(state):
 #   if len(state.my_fleets()) >= 1:
  #      return False
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    highest_priority=0
    min_source_planet=None
    min_dst_planet=None    
    max_growth_rate=0
    required_ships_final =0
    for my_planet in state.my_planets():
        for neutral_planet in neutral_planets:
            required_ships = neutral_planet.num_ships+1
            priority=neutral_planet.growth_rate/state.distance(my_planet.ID, neutral_planet.ID)
            if(my_planet.num_ships>neutral_planet.num_ships):
                if (priority>highest_priority)  or (priority==highest_priority and required_ships<required_ships_final):
                    min_source_planet=my_planet
                    min_dst_planet=neutral_planet
                    required_ships_final =required_ships
                    highest_priority=priority
        for target_planet in enemy_planets:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            priority=2*target_planet.growth_rate/state.distance(my_planet.ID, target_planet.ID)
            if(my_planet.num_ships>required_ships):
                if (priority>highest_priority)  or (priority==highest_priority and required_ships<required_ships_final):
                    min_source_planet=my_planet
                    min_dst_planet=target_planet
                    required_ships_final =required_ships
                    highest_priority=priority

    if not min_source_planet or not min_dst_planet:
        return False
    else:
        
        return issue_order(state,min_source_planet.ID, min_dst_planet.ID, required_ships_final)
