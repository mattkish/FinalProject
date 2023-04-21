
CREATE TABLE IF NOT EXISTS planets (
    planet_name VARCHAR(60),
    mass REAL,
    radius REAL,
    planet_period REAL,
    semi_major_axis REAL,
    temperature REAL,
    distance_light_year REAL,
    host_star_mass REAL,
    host_star_temperature REAL
);


CREATE TABLE IF NOT EXISTS cats (
    origin_id INTEGER,
    general_health INTEGER,
    min_weight INTEGER,
    max_weight INTEGER,
    min_life_expectancy INTEGER,
    max_life_expectancy INTEGER,
    cat_name VARCHAR(60),
    FOREIGN KEY (origin_id) REFERENCES origins(id)
);

CREATE TABLE IF NOT EXISTS origins (
    id INTEGER,
    origin VARCHAR(60),
    PRIMARY KEY (id)
);