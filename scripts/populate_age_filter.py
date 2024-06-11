from pprint import pprint
import csv
import psycopg2
import os
from psycopg2.extras import Json
psycopg2.extras.register_uuid()
import uuid
from urllib.parse import urlparse
import traceback

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


with open('20240508 YourPeer Age and Population Served sheet - 20240508.csv') as f:
    rows = [
        {
            'should_process': bool(row['eligible_values']['age_max'] or \
                row['eligible_values']['age_min'] or \
                row['eligible_values']['all_ages']),
            **row
        } for row in 
        [ 
            {
                'eligible_values' : {
                    'population_served': None if row['Population served'] == '' else row['Population served'],
                    'age_max' : None if row['Age max (inclusive)'] in ('', '?') else int(row['Age max (inclusive)']) + 1,
                    'age_min': None if row['Age min'] == '' else int(row['Age min']),
                    'all_ages': bool(row['All ages']),
                },
                'gogetta_url': row['gogetta_link service'],
                'row_num': row_num + 1,
            }
            for row_num, row in enumerate(csv.DictReader(f))
        ]
    ]

print('number of rows', len(rows))
#pprint(rows)

def validate_service_id(service_id):
    uuid_service_id = uuid.UUID(service_id)
    # verify that service exists
    cur.execute('select count(1) from services where id = %s', (service_id, ))
    assert cur.fetchone()[0] == 1

with open('out.csv', 'w') as f:

    writer = csv.DictWriter(f, 
        fieldnames=['status'] + 
            list(rows[0].keys()))
    writer.writeheader()

    for i, row in enumerate(rows): 
        if not row['should_process']:
            writer.writerow({
                'status': f'SKIP: no age min, age max, or all ages data',
                **row
            })
            continue

        # do a quick sanity check
        eligible_values = row['eligible_values']

        try:
            service_id = urlparse(row['gogetta_url']).path.split('/')[-1]
            validate_service_id(service_id)
        except:
            writer.writerow({
                'status': f'ERROR: Unable to find a service_id for given row: {traceback.format_exc()}',
                **row
            })
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
            cur.execute('''
                update eligibility
                    set eligible_values = %s
                    where parameter_id = %s and service_id = %s
            ''', (
                Json(existing_eligible_values + [eligible_values]),
                age_parameter_id,
                service_id,
            ))
        else:
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
                Json([eligible_values]),
                age_parameter_id,
                service_id,
            ))


        #cur.execute("SELECT * FROM services where id = %s", (service_id,))
        conn.commit()

        writer.writerow({
            'status': 'SUCCESS',
            **row
        })

        #x = cur.execute(f"SELECT * FROM locations where id = '{location_id}'")
        #print(i, x, row)
        #cur.execute("SELECT * FROM locations where id = $1", (row['location_id'],))

