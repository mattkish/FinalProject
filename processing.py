import sqlite3
import os
from api_and_database import create_database, add_planet_data, add_cat_data, api_planets, api_cat, connect_database
import matplotlib.pyplot as plt


def main():
    
    #cur, conn = connect_database('data.db')
    #cur.execute("SELECT {} FROM sqlite_master WHERE type='table' AND name='{}'", 'planets', )
    cur, conn = create_database('data.db')
    
    planet_data = []
    cat_data = []
    
    cur.execute('SELECT COUNT(*) FROM planets')
    x = cur.fetchone()[0]
    
    if x <= 75:
        for i in range(x, x+25):
            # storing one at a time
            planet_data.append(api_planets(i))
    # x = api_planets(3)
    # planet_data += x[:10]
        add_planet_data(cur, conn, planet_data)


    cur.execute('SELECT COUNT(*) FROM cats')
    y = cur.fetchone()[0]
    if y <= 50:
        for i in range(y, y+25):
            # storing one at a time
            cat_data.append(api_cat(i))
        add_cat_data(cur, conn, cat_data)

    cur.execute('SELECT COUNT(*) FROM planets')
    count100 = cur.fetchone()[0]
    if count100 == 100:
        cur.execute('''
                    SELECT origins.origin, AVG(cats.general_health) as average_health, max_weight, cat_name, general_health
                    FROM cats
                    JOIN origins ON cats.origin_id = origins.id
                    GROUP BY origins.origin
                    ORDER BY average_health DESC
                    ''')

        origin_health_data = cur.fetchall()

        with open('output.txt', 'w') as f:
            f.write("Origin, Average Health, Max Weight, General Health\n")
            for row in origin_health_data:
                f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[4]}\n")

        cur.execute('''
                    SELECT planet_name, mass, temperature, host_star_temperature, host_star_mass, radius
                    FROM planets
                    ORDER BY mass DESC
                    ''')

        planet_data = cur.fetchall()

        with open('planet_output.txt', 'w') as f:
            f.write(
                "Planet Name, Mass, Temperature, Host Star Temperature, Host Star Mass, Radius\n")
            for row in planet_data:
                f.write(
                    f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]} \n")

        cur.execute(''' 
                    SELECT planet_name, mass, temperature, host_star_temperature, host_star_mass, radius
                    FROM planets
                    WHERE radius > 0.01
                    ORDER BY radius DESC
                    ''')
        planet_rad = cur.fetchall()
        with open('planet_radius.txt', 'w') as f:
            f.write(
                "Planet Name, Mass, Temperature, Host Star Temperature, Host Star Mass, Radius\n")
            for row in planet_rad:
                f.write(
                    f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]} \n")

        origins = [row[0] for row in origin_health_data]
        avg_health = [row[1] for row in origin_health_data]
        max_weight = [row[2] for row in origin_health_data]
        cat_name = [row[3] for row in origin_health_data]
        plt.bar(origins, avg_health, color='purple')
        plt.xlabel('Origin')
        plt.ylabel('Average Health')
        plt.title('Average Health by Cat Origin')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('visualization1.png')
        plt.show()

        plt.stem(cat_name, max_weight)
        plt.axis('equal')
        plt.title('Maximum Weight For Each Cat Type')
        plt.xticks(range(len(cat_name)), cat_name, rotation=90)
        plt.tick_params(axis='x', labelsize=6)

        plt.savefig('visualization2.png')
        plt.show()

        planet_name = [row[0] for row in planet_data]
        planet_mass = [row[1] for row in planet_data]
        planet_temp = [row[2] for row in planet_data]
        star_temp = [row[3] for row in planet_data]
        star_mass = [row[4] for row in planet_data]
        planet_radius = [row[5] for row in planet_data]

        plt.scatter(planet_mass, star_mass)
        plt.xlabel('Planet Mass')
        plt.ylabel('Star Mass')
        plt.title("How a Star's Mass affects Planet Mass")
        plt.savefig('visualization3.png')
        plt.show()

        plt.scatter(planet_radius, planet_mass, color='purple')
        plt.xlabel('Planet Radius')
        plt.ylabel('Planet Mass')
        plt.ylim(0, 3)
        plt.title('Planet Radius vs Planet Mass')
        plt.savefig('visualization4.png')
        plt.show()


if __name__ == '__main__':
    main()
