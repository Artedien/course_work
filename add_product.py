from dataclasses import dataclass
import time

from database import db_session
from models import ozon_base
from ozon_parser import parse

coffe_machines = parse()


def write_in_base(data):
   db_session.bulk_insert_mappings(ozon_base,coffe_machines)
   db_session.commit()
    

if __name__ == "__main__":
    start = time.time()
    write_in_base(coffe_machines)
    print(f'Загрузка заняла {time.time()-start} сек')