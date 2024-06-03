from pprint import pprint
import csv
import psycopg2
import os
from psycopg2.extras import Json
psycopg2.extras.register_uuid()
import uuid

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

cur.execute("select id from eligibility_parameters where name = 'age'")
age_parameter_id = cur.fetchone()[0]


# reset db (for test purposes only)
# FIXME: disable this line
cur.execute("delete from eligibility where parameter_id = %s", (age_parameter_id,))
conn.commit()

with open('20240508 YourPeer Age and Population Served sheet - services.csv') as f:
    rows = [ 
        {
            'eligible_values' : {
                'populationServed': None if row['Population served'] == '' else row['Population served'],
                'ageMax' : None if row['Age max (inclusive)'] in ('', '?') else int(row['Age max (inclusive)']) + 1,
                'ageMin': None if row['Age min'] == '' else int(row['Age min']),
                'allAges': bool(row['All ages']),
            },
            'location_id': row['location_id'],
            'service_id': row['id'],
            'service_name': row['service_name'],
        }
        for row in csv.DictReader(f)
    ]

#pprint(rows)

for i, row in enumerate(rows): 
    # do a quick sanity check
    service_id = row['service_id']
    location_id = row['location_id']
    eligible_values = row['eligible_values']

    # validate the uuid (there are some malformed ones)
    print(location_id, service_id)
    try: 
        uuid_location_id = uuid.UUID(location_id)
    except:
        print('Malformed location id', location_id)
        continue
    try: 
        uuid_service_id = uuid.UUID(service_id)
    except:
        print('Malformed location id', service_id)
        continue

    # accumulate results. If there's already a row in the database, append another age filter to him
    cur.execute('''
        select eligible_values from eligibility where parameter_id = %s and service_id = %s
    ''', (
        age_parameter_id,
        service_id,
    ))
    existing_row = cur.fetchone()
    if existing_row:
        existing_eligible_values = existing_row[0]
        assert type(existing_eligible_values) == list
        eligible_values = existing_eligible_values + eligible_values


    #cur.execute("SELECT * FROM services where id = %s", (service_id,))
    cur.execute("""
        select sal.service_id from service_at_locations sal
        inner join services s on sal.service_id = s.id
        where s.name = %s and sal.location_id = %s
    """, (row['service_name'],row['location_id'],))
    service_id = cur.fetchone()
    if not service_id:
        print('Unable to find service id for location and service name', row['service_name'],row['location_id'])
        continue
    service_id = service_id[0]

    cur.execute('''
        insert into eligibility
            (
                id,
                eligible_values,
                created_at,
                updated_at,
                parameter_id,
                service_id
            )
            values(
                gen_random_uuid(),
                %s,
                NOW(),
                NOW(),
                %s,
                %s
            )
    ''', (
        Json(eligible_values),
        age_parameter_id,
        service_id,
    ))
    conn.commit()

    #x = cur.execute(f"SELECT * FROM locations where id = '{location_id}'")
    #print(i, x, row)
    #cur.execute("SELECT * FROM locations where id = $1", (row['location_id'],))

