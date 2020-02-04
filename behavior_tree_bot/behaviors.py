import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def attack_closest_enemy_planet(state):
    min_distance=0
    min_source_planet=None
    min_dst_planet=None    
    required_ships_final =0
    if len(state.my_fleets()) >= 1:
        return False
    for my_planet in state.my_planets():
        for target_planet in state.enemy_planets():
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            if(my_planet.num_ships>=required_ships):
                if (state.distance(my_planet.ID, target_planet.ID)<min_distance) or (min_distance==0):
                    min_distance=state.distance(my_planet.ID, target_planet.ID)
                    min_source_planet=my_planet
                    min_dst_planet=target_planet
                    required_ships_final =required_ships
    if not min_source_planet or not min_dst_planet:
        return False
    else:
        return issue_order(state,min_source_planet.ID, min_dst_planet.ID, required_ships_final)

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
  #  if len(state.my_fleets()) >= 1:
   #     return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_closest_neutral_planet(state):
    if len(state.my_fleets()) >= 1:
        return False
    min_distance=0
    min_source_planet=None
    min_dst_planet=None
    for my_planet in state.my_planets():
        for neutral_planet in state.neutral_planets():
            if(my_planet.num_ships>neutral_planet.num_ships):
                if (state.distance(my_planet.ID, neutral_planet.ID)<min_distance) or (min_distance==0):
                    min_distance=state.distance(my_planet.ID, neutral_planet.ID)
                    min_source_planet=my_planet
                    min_dst_planet=neutral_planet


    if not min_source_planet or not min_dst_planet:
        return False
    else:
        return issue_order(state,min_source_planet.ID, min_dst_planet.ID, min_dst_planet.num_ships+1)

def spread_to_closest_all_planet(state):
 #   if len(state.my_fleets()) >= 1:
  #      return False
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    min_distance=0
    min_source_planet=None
    min_dst_planet=None    
    required_ships_final =0
    for my_planet in state.my_planets():
        for neutral_planet in neutral_planets:
            required_ships = neutral_planet.num_ships+1
            if(my_planet.num_ships>neutral_planet.num_ships):
                if (state.distance(my_planet.ID, neutral_planet.ID)<min_distance) or (min_distance==0):
                    min_distance=state.distance(my_planet.ID, neutral_planet.ID)
                    min_source_planet=my_planet
                    min_dst_planet=neutral_planet
                    required_ships_final =required_ships
        for target_planet in enemy_planets:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            if(my_planet.num_ships>=required_ships):
                if (state.distance(my_planet.ID, target_planet.ID)<min_distance) or (min_distance==0):
                    min_distance=state.distance(my_planet.ID, target_planet.ID)
                    min_source_planet=my_planet
                    min_dst_planet=target_planet
                    required_ships_final =required_ships



    if not min_source_planet or not min_dst_planet:
        return False
    else:
        
        return issue_order(state,min_source_planet.ID, min_dst_planet.ID, required_ships_final)

def spread_from_strongest_to_closest_neutral_planet(state):
    if len(state.my_fleets()) >= 1:
        return False    
    min_distance=0
    min_source_planet=None
    min_dst_planet=None
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    for neutral_planet in state.neutral_planets():
        if(strongest_planet.num_ships>neutral_planet.num_ships):
            if (state.distance(strongest_planet.ID, neutral_planet.ID)<min_distance) or (min_distance==0):
                min_distance=state.distance(strongest_planet.ID, neutral_planet.ID)
                min_dst_planet=neutral_planet
    if not min_dst_planet:
        return False
    else:
        return issue_order(state,strongest_planet.ID, min_dst_planet.ID, min_dst_planet.num_ships+1)