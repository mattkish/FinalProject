DROP TABLE IF EXISTS planets;
CREATE TABLE planets (
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

DROP TABLE IF EXISTS cats;
CREATE TABLE cats (
    origin_id INTEGER,
    family_friendly INTEGER,
    shedding INTEGER,
    general_health INTEGER,
    playfulness INTEGER,
    children_friendly INTEGER,
    grooming INTEGER,
    intelligence INTEGER,
    other_pets_friendly INTEGER,
    min_weight INTEGER,
    max_weight INTEGER,
    min_life_expectancy INTEGER,
    max_life_expectancy INTEGER,
    cat_name VARCHAR(60),
    FOREIGN KEY (origin_id) REFERENCES origins(id)
);

DROP TABLE IF EXISTS origins;
CREATE TABLE origins (
    id INTEGER,
    origin VARCHAR(60),
    PRIMARY KEY (id)
);