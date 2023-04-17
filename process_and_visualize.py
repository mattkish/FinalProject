import sqlite3
import os
from api_and_database import create_database, add_planet_data, add_cat_data, api_planets, api_cat
import matplotlib.pyplot as plt

def main():
    cur, conn = create_database('data.db')

    for i in range(0, 100, 10):
        planet_data = api_planets(i)
        add_planet_data(cur, conn, planet_data)

        cat_data = api_cat(i)
        add_cat_data(cur, conn, cat_data)

    # Part 3 - Process the data for cats
    cur.execute('''
    SELECT origins.origin, AVG(cats.general_health) as avg_health
    FROM cats
    JOIN origins ON cats.origin_id = origins.id
    GROUP BY origins.origin
    ORDER BY avg_health DESC
    ''')

    origin_health_data = cur.fetchall()

    with open('output.txt', 'w') as f:
        f.write("Origin, Average Health\n")
        for row in origin_health_data:
            f.write(f"{row[0]}, {row[1]}\n")

    # Part 3 - Process the data for planets
    cur.execute('''
    SELECT ROUND(AVG(temperature), 2) as avg_temperature, COUNT(*) as num_planets
    FROM planets
    GROUP BY CASE
        WHEN temperature < 1000 THEN '<1000'
        WHEN temperature BETWEEN 1000 AND 2000 THEN '1000-2000'
        WHEN temperature BETWEEN 2000 AND 3000 THEN '2000-3000'
        ELSE '>3000'
    END
    ''')

    temperature_data = cur.fetchall()

    with open('planet_output.txt', 'w') as f:
        f.write("Temperature Range, Average Temperature, Number of Planets\n")
        for row in temperature_data:
            f.write(f"{row[0]}, {row[1]}, {row[2]}\n")

    # Part 4 - Visualize the data for cats
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
    temperature_ranges = ['<1000', '1000-2000', '2000-3000', '>3000']
    avg_temperatures = [row[0] for row in temperature_data]
    num_planets = [row[1] for row in temperature_data]

    plt.bar(temperature_ranges, avg_temperatures, color='blue')
    plt.xlabel('Temperature Range (K)')
    plt.ylabel('Average Temperature (K)')
    plt.title('Average Temperature by Range')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('visualization3.png')
    plt.show()

    plt.pie(num_planets, labels=temperature_ranges, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Percentage Distribution of Number of Planets by Temperature Range')
    plt.tight_layout()
    plt.savefig('visualization4.png')
    plt.show()

if __name__ == '__main__':
    main()