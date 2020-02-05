import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging, traceback, sys, os, inspect


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
    max_growth_rate=0
    # if len(state.my_fleets()) >= 1:
    #     logging.info('Fleet already sents\n-----------------------------------------------------------')
    #     return False
    for my_planet in state.my_planets():
        for target_planet in state.enemy_planets():
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            if(my_planet.num_ships>=required_ships):
                if (state.distance(my_planet.ID, target_planet.ID)<min_distance) or (min_distance==0) or ((state.distance(my_planet.ID, target_planet.ID)==min_distance) and max_growth_rate<(target_planet.growth_rate*2)):
                    min_distance=state.distance(my_planet.ID, target_planet.ID)
                    min_source_planet=my_planet
                    min_dst_planet=target_planet
                    required_ships_final =required_ships
                    max_growth_rate=(target_planet.growth_rate*2)
    if not min_source_planet or not min_dst_planet:
        logging.info('No new  target\n-----------------------------------------------------------')
        return False
    else:
        logging.info('ATTACK\n-----------------------------------------------------------')
        return issue_order(state,min_source_planet.ID, min_dst_planet.ID, required_ships_final)

def attack_highest_enemy_growth_rate(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the fastest enemy planet.
    fastest_growth_rate = 0
    for planet in state.enemy_planets():
        if planet.growth_rate > fastest_growth_rate and planet.num_ships < strongest_planet.num_ships:
            fastest_growth_rate = planet.growth_rate
            fastest_planet = planet

    if not strongest_planet or not fastest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, fastest_planet.ID, strongest_planet.num_ships / 2)

def attack_weighted(state):
    growth_rate_weight = 10
    num_ships_weight = 2
    my_planet_strength_weight = 1
    distance_weight = 1
    ship_ratio = 7 / 8
    growth_adjustment = 2
    enemy_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships, reverse=True)
    my_planets = [planet for planet in state.my_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]
    my_planets.sort(key=lambda p: p.num_ships)

    # if len(state.my_fleets()) >= 1:
    #     return False
    most_weight = None
    most_weight_planet = None
    spreading_planet = None
    should_attack = False
    for my_planet in my_planets:
        for target_planet in enemy_planets:
            estimated_requirement = target_planet.num_ships + \
                             state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate * growth_adjustment + 1
            # estimated_requirement = 10
            weight = (growth_rate_weight * target_planet.growth_rate) + (num_ships_weight * target_planet.num_ships * -1) + \
                     (distance_weight * (state.distance(my_planet.ID, target_planet.ID)) * -1) + \
                     (my_planet_strength_weight * my_planet.num_ships)
            if most_weight is None:
                most_weight_planet = target_planet
                spreading_planet = my_planet
                most_weight = weight
                required_ships = estimated_requirement + 1
                if my_planet.num_ships * ship_ratio > estimated_requirement:
                    should_attack = True
            if (my_planet.num_ships * ship_ratio > estimated_requirement) and (weight > most_weight):
                logging.info('Found new target\n-----------------------------------------------------------')
                should_attack = True
                most_weight_planet = target_planet
                spreading_planet = my_planet
                most_weight = weight
                required_ships = estimated_requirement + 1
                # issue_order(state, spreading_planet.ID, most_weight_planet.ID, required_ships)
    if not spreading_planet or not most_weight_planet or not should_attack:
        logging.info('No attack --------------------------------------------------------------------')
        # No legal source or destination
        return False
    else:
        logging.info('--------------------------------------------------------------- ACTUAL ATTACK')
        logging.info("Stats (My num ships | Enemy num ships | Attack size | Distance | Enemy growth:\n" + \
                     ' '.join([str(spreading_planet.num_ships), str(most_weight_planet.num_ships), str(required_ships), \
                               str(state.distance(my_planet.ID, most_weight_planet.ID)), str(most_weight_planet.growth_rate)]))
        return issue_order(state, spreading_planet.ID, most_weight_planet.ID, required_ships)


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
    max_growth_rate=0
    required_ships_final =0
    for my_planet in state.my_planets():
        for neutral_planet in neutral_planets:
            required_ships = neutral_planet.num_ships+1
            if(my_planet.num_ships>neutral_planet.num_ships):
                if (state.distance(my_planet.ID, neutral_planet.ID)<min_distance) or (min_distance==0) or ((state.distance(my_planet.ID, neutral_planet.ID)==min_distance) and max_growth_rate<neutral_planet.growth_rate):
                    min_distance=state.distance(my_planet.ID, neutral_planet.ID)
                    min_source_planet=my_planet
                    min_dst_planet=neutral_planet
                    required_ships_final =required_ships
                    max_growth_rate=neutral_planet.growth_rate
        # for target_planet in enemy_planets:
        #     required_ships = target_planet.num_ships + \
        #                          state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
        #     if(my_planet.num_ships>=required_ships):
        #         if (state.distance(my_planet.ID, target_planet.ID)<min_distance) or (min_distance==0) or ((state.distance(my_planet.ID, target_planet.ID)==min_distance) and max_growth_rate<(target_planet.growth_rate*2)):
        #             min_distance=state.distance(my_planet.ID, target_planet.ID)
        #             min_source_planet=my_planet
        #             min_dst_planet=target_planet
        #             required_ships_final =required_ships
        #             max_growth_rate=(target_planet.growth_rate*2)



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

def spread_weighted(state):
    growth_rate_weight = 0
    num_ships_weight = 1
    distance_weight = 1
    if len(state.my_fleets()) >= 1:
        return False
    spreading_planet = None
    most_weight_planet = None
    most_weight = None
    for my_planet in state.my_planets():
        for target_planet in state.neutral_planets():
            estimated_requirement = target_planet.num_ships
            weight = (growth_rate_weight * target_planet.growth_rate) + (num_ships_weight * target_planet.num_ships * -1) + \
                     (distance_weight * state.distance(my_planet.ID, target_planet.ID) * -1)
            if most_weight is None:
                most_weight_planet = target_planet
                spreading_planet = my_planet
                most_weight = weight
                required_ships = estimated_requirement + 1
            if (my_planet.num_ships > estimated_requirement) and (weight > most_weight):
                most_weight_planet = target_planet
                spreading_planet = my_planet
                most_weight = weight
                required_ships = estimated_requirement + 1
    if not spreading_planet or not most_weight_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, spreading_planet.ID, most_weight_planet.ID, required_ships)