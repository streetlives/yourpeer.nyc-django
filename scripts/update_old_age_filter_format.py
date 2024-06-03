from pprint import pprint
import psycopg2
import os
from geopy.geocoders import GoogleV3
from psycopg2.extras import Json

# Connect to your postgres DB
conn = psycopg2.connect(
    dbname=os.environ.get('DATABASE_NAME'),
    user=os.environ.get('DATABASE_USER'),
    password=os.environ.get('DATABASE_PASSWORD'),
    host=os.environ.get('DATABASE_HOST'),
    port=os.environ.get('DATABASE_PORT'),
)

# Open a cursor to perform database operations
cur = conn.cursor()


def parse_old_eligible_values(eligible_values):
    if eligible_values == ["13-19"]:
        return {
            "ageMin": 13,
            "ageMax": 20,
        }
    elif eligible_values == ["18-24"]:
        return {
            "ageMin": 18,
            "ageMax": 25,
        }
    elif eligible_values == ["18+"]:
        return {
            "ageMin": 18,
        }
    elif eligible_values == ["children"]:
        return {
            "ageMax": 18,
            "populationServed": 'children'
        }

# first update the old eligibility parameters to the new format
cur.execute('''
  select id, eligible_values from eligibility where parameter_id = 
    (select id from eligibility_parameters where name = 'age')
''')
for id, eligible_values in cur.fetchall():
    print(id)
    # parse the eligible_values
    cur.execute('''
      update eligibility
        set eligible_values = %s 
        where id = %s 
    ''', (Json(parse_old_eligible_values(eligible_values)), id,))
    conn.commit()

    
