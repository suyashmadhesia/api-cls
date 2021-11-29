import uuid
import random


def base():
    return str(random.randint(10, 99))

def generate_uid():
    uid = base() + str(uuid.uuid1()) + base()