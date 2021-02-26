"""Does the main job on transferring data to posgresql """

import argparse
from time import gmtime, strftime
import json

from postgres_database import PostgreSQL
from airtables import *
from SETTINGS import *


postgres = PostgreSQL(
        login =  POSTGRES_LOGIN,
        password = POSGRES_PASSWORD,
        host = POSTGRES_HOST,
        base = POSTGRES_DATABASE,
        port = POSTGRES_PORT

)

airtables_data = data = get_airtables_data(AIRTABLES_TOKEN=AIRTABLES_TOKEN,
                                           AIRTABLES_ID=AIRTABLES_ID)

if __name__ == '__main__':
    postgres.create_tables()
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ids = [f"'{i[0]}'" for i in airtables_data]

    postgres.create_tables()


    postgres.insert(table='airtables_therapists',
              columns=['id', 'name', 'methods', 'photo'],
              values=airtables_data
              )

    postgres.delete(table='airtables_therapists',
                    ids =ids )

    postgres.insert(table='airtables_dumps',
              columns=['date', 'loaded_data'],
              values=[[current_time, json.dumps(airtables_data)]]
              )




    # parser = argparse.ArgumentParser()
    # parser.add_argument("-att", "--AirtablesToken", help="Token for airtables")
    # parser.add_argument("-ati", "--AirtablesId", help="IdForAirtables")
    # parser.add_argument("-pghost", "--PostgresHost", help="Show Output")
    # parser.add_argument("-pgport", "--PostgresPort", help="Show Output")
    # parser.add_argument("-pgbase", "--PostgresDatabase", help="postgres database name")
    # parser.add_argument("-pglogin", "--PosgresLogin", help="Show Output")
    # parser.add_argument("-ppass", "--PosgresPassword", help="Show Output")
    # args = parser.parse_args()
    #
    # postgres = PostgreSQL(
    #     login=args.PosgresLogin or POSTGRES_LOGIN,
    #     password=args.PosgresPassword or POSGRES_PASSWORD,
    #     host=args.PostgresHost or POSTGRES_HOST,
    #     base=args.PostgresDatabase or POSTGRES_DATABASE,
    #     port=args.PosgresPassword or POSGRES_PASSWORD
    #
    # )
    #
    # airtables_data = data = get_airtables_data(AIRTABLES_TOKEN=AIRTABLES_TOKEN,
    #                                            AIRTABLES_ID=AIRTABLES_ID)

