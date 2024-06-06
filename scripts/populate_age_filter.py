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

with open('20240508 YourPeer Age and Population Served sheet - services.csv') as f:
    rows = [
        {
            'should_process': bool(row['eligible_values']['ageMax'] or \
                row['eligible_values']['ageMin'] or \
                row['eligible_values']['allAges']),
            **row
        } for row in 
        [ 
            {
                'eligible_values' : {
                    'populationServed': None if row['Population served'] == '' else row['Population served'],
                    'ageMax' : None if row['Age max (inclusive)'] in ('', '?') else int(row['Age max (inclusive)']) + 1,
                    'ageMin': None if row['Age min'] == '' else int(row['Age min']),
                    'allAges': bool(row['All ages']),
                },
                'location_id': row['location_id'],
                'service_name': row['service_name'],
                'gogetta_url': row['GoGetta URL'],
                'organization_id': row['id'],
                'organization_name': row['Org name'],
                'location_name': row['location_name'],
                'row_num': row_num + 1,
            }
            for row_num, row in enumerate(csv.DictReader(f))
        ]
    ]

print('number of rows', len(rows))
#pprint(rows)

def validate_location_id(location_id):
    uuid_location_id = uuid.UUID(location_id)
    # verify that location exists
    cur.execute('select count(1) from locations where id = %s', (location_id, ))
    assert cur.fetchone()[0] == 1

def validate_organization_id(organization_id):
    uuid_organization_id = uuid.UUID(organization_id)
    # verify that organization exists
    cur.execute('select count(1) from organizations where id = %s', (organization_id, ))
    assert cur.fetchone()[0] == 1

with open('out.csv', 'w') as f:

    writer = csv.DictWriter(f, 
        fieldnames=['status', 'derived_location_id', 'derived_service_id'] + 
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
        location_id = row['location_id']
        eligible_values = row['eligible_values']

        errors = []

        # validate the uuid (there are some malformed ones)
        try: 
            validate_location_id(location_id)
        except:
            errors.append(traceback.format_exc())
            print(traceback.format_exc())
            # if that doesn't work, try to look up the location by parsing GoGetta URL
            try:
                location_id = urlparse(row['gogetta_url']).path.split('/')[-1]
                validate_location_id(location_id)
            except:
                errors.append(traceback.format_exc())
                print(traceback.format_exc())
                try:
                    # if that doesn't work, then try to look up the location by organization id and location name
                    organization_id = row['organization_id']
                    location_name = row['location_name']
                    validate_organization_id(organization_id)
                    cur.execute("""
                        select id::varchar as location_id from locations
                        where organization_id = %s and name = %s
                    """, (organization_id, location_name,))
                    location_id = cur.fetchone()[0]
                except:
                    errors.append(traceback.format_exc())
                    print(traceback.format_exc())
                    # if that doesn't work, then try to look up the location by organization name and location name
                    try:
                        organization_name = row['organization_name']
                        cur.execute("""
                            select l.id::varchar as location_id 
                            from locations l inner join organizations o 
                            on l.organization_id = o.id
                            where o.name = %s and l.name = %s
                        """, (organization_name, location_name,))
                        location_id = cur.fetchone()[0]
                    except:
                        errors.append(traceback.format_exc())
                        print(traceback.format_exc())
                        writer.writerow({
                            'status': f'ERROR: Unable to find a location_id for given row: {";".join(errors)}',
                            'derived_location_id': None, 
                            'derived_service_id': None,
                            **row
                        })
                        continue

        # now that we have a location_id, look up the service id from the location_id and service name
        service_name = row['service_name']
        cur.execute("""
            select sal.service_id from service_at_locations sal
            inner join services s on sal.service_id = s.id
            where s.name = %s and sal.location_id = %s
        """, (service_name, location_id,))
        service_id = cur.fetchone()
        if not service_id:
            writer.writerow({
                'status': f'ERROR: Unable to find service id for location and service name: {service_name} {location_id}',
            'derived_location_id': location_id, 
            'derived_service_id': None,
                **row
            })
            continue
        service_id = service_id[0]


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
            print(existing_eligible_values)
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
            'derived_location_id': location_id, 
            'derived_service_id': service_id,
            **row
        })

        #x = cur.execute(f"SELECT * FROM locations where id = '{location_id}'")
        #print(i, x, row)
        #cur.execute("SELECT * FROM locations where id = $1", (row['location_id'],))

