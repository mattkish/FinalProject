import sqlite3
import os
from api_and_database import create_database, add_planet_data, add_cat_data, api_planets, api_cat
import matplotlib.pyplot as plt

def main():
    cur, conn = create_database('data.db')
    planet_data = []
    cat_data = []
    # putting 100 things in planet database
    for i in range(0, 3):
        planet_data += api_planets(i)
    x = api_planets(3)
    planet_data += x[:10]
    add_planet_data(cur, conn, planet_data)
    
    for i in range(0, 5):
        cat_data += api_cat(i)
        add_cat_data(cur, conn, cat_data)

    cur.execute('''
                SELECT origins.origin, AVG(cats.general_health) as average_health
                FROM cats
                JOIN origins ON cats.origin_id = origins.id
                GROUP BY origins.origin
                ORDER BY average_health DESC
                ''')

    origin_health_data = cur.fetchall()

    with open('output.txt', 'w') as f:
        f.write("Origin, Average Health\n")
        for row in origin_health_data:
            f.write(f"{row[0]}, {row[1]}\n")

# change this to calculate correlation between mass and radius or something
    cur.execute('''
                SELECT planet_name, mass, temperature, host_star_temperature, host_star_mass
                FROM planets
                ORDER BY mass DESC
                ''')

    planet_data = cur.fetchall()


    with open('planet_output.txt', 'w') as f:
        f.write("Planet Name, Mass, Temperature, Host Star Temperature, Host Star Mass\n")
        for row in planet_data:
            print (planet_data)
            f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]} \n")

    origins = [row[0] for row in origin_health_data]
    avg_health = [row[1] for row in origin_health_data]

    plt.bar(origins, avg_health, color='purple')
    plt.xlabel('Origin')
    plt.ylabel('Average Health')
    plt.title('Average Health by Cat Origin')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('visualization1.png')
    plt.show()

    plt.pie(avg_health, labels=origins, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Percentage Distribution of Average Health by Cat Origin')
    plt.tight_layout()
    plt.savefig('visualization2.png')
    plt.show()
    # Part 4 - Visualize the data for planets
    planet_name = [row[0] for row in planet_data]
    planet_mass = [row[1] for row in planet_data]
    planet_temp = [row[2] for row in planet_data]
    star_temp = [row[3] for row in planet_data]
    star_mass = [row[3] for row in planet_data]

    print(len(planet_name))
    print(len(planet_mass))
    plt.scatter(planet_mass, star_mass)
    plt.xlabel('Planet Mass')
    plt.ylabel('Star Mass')
    plt.title('How Star Mass effects Planet Mass')
    plt.tight_layout()
    plt.savefig('visualization3.png')
    plt.show()
    print(star_temp)
    print(star_mass)

    plt.bar(planet_temp, star_temp)
    plt.axis('equal')
    plt.title('Percentage Distribution of Number of Planets by Temperature Range')
    plt.tight_layout()
    plt.savefig('visualization4.png')
    plt.show()

if __name__ == '__main__':
    main()