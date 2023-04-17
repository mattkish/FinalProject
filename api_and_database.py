import matplotlib.pyplot as plt
import sqlite3
import requests
import json
import os


# def api_muscles(muscle, offset):
#     offset = 10
#     api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&offset={}'.format(muscle, offset)
#     response = requests.get(api_url, headers={'X-Api-Key': 'a88gHCFRZ4fM7clDyz+Y/w==6tkJTF9SubqVB3Ds'})
#     if response.status_code == requests.codes.ok:
#         return response.json()
#         #  return json.loads(response.text)
#     else:
#         print("Error:", response.status_code, response.text)

def create_database(database):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database)
    cur = conn.cursor()
    
    with open("data.sql", 'r') as f:
        schema = f.read().split(';')
    
    for statement in schema:
        if statement.strip(): 
            cur.execute(statement)
    
    return cur, conn


def api_planets(offset):
    min_mass = 0.01
    api_url = 'https://api.api-ninjas.com/v1/planets?min_mass={}&offset={}'.format(min_mass, offset)
    response = requests.get(api_url, headers={'X-Api-Key': 'a88gHCFRZ4fM7clDyz+Y/w==6tkJTF9SubqVB3Ds'})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)    

def api_cat(offset):
    min_weight = 0.01
    api_url = 'https://api.api-ninjas.com/v1/cats?min_weight={}&offset={}'.format(min_weight, offset)
    response = requests.get(api_url, headers={'X-Api-Key': 'a88gHCFRZ4fM7clDyz+Y/w==6tkJTF9SubqVB3Ds'})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)

def add_planet_data(cur, conn, planet_data):
    for d in planet_data:
        cur.execute('''
                    INSERT OR IGNORE INTO 
                    planets (planet_name, mass, radius, planet_period, semi_major_axis, temperature, distance_light_year, host_star_mass, host_star_temperature)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (d['name'], d['mass'], d['radius'], d['period'], d['semi_major_axis'], d['temperature'], d['distance_light_year'], d['host_star_mass'], d['host_star_temperature'],))
    conn.commit()

def add_cat_data(cur, conn, cat_data):
    origins = []
    for d in cat_data:
        cur.execute(''' 
                    INSERT OR IGNORE INTO 
                    cats (origin_id, cat_name, family_friendly, shedding, general_health, playfulness, children_friendly, grooming, intelligence, other_pets_friendly, min_weight, max_weight, min_life_expectancy, max_life_expectancy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (get_origin_id(origins, d['origin']), d.get('name', None), d.get('family_friendly', None), d.get('shedding', None), d.get('general_health', None), d.get('playfulness', None), d.get('children_friendly', None), d.get('grooming', None), d.get('intelligence', None), d.get('other_pets_friendly', None), d.get('min_weight', None), d.get('max_weight', None), d.get('min_life_expectancy', None), d.get('max_life_expectancy', None),))
        cur.execute('INSERT OR IGNORE INTO origins (id, origin) VALUES (?, ?)', (get_origin_id(origins, d['origin']), d['origin']))
    conn.commit()
    
def get_origin_id(origins, origin):
    if origin not in origins:
        origins.append(origin)
    for i, origin_item in enumerate(origins):
        if origin == origin_item:
            origin_id = i
    return origin_id
        
    


    

        


