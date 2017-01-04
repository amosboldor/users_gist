import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel


USERS = [
    {'first_name': 'Amos',
     'last_name': 'Boldor',
     'user_name': 'amos',
     'email': 'amosboldor@gmail.com',
     'fav_food': 'pizza',
     'password': '$6$rounds=656000$a5pan8c0v4eFY62j$HzroucGwrxR8QjJW9U5eEKkKAVrKe6OoMuWCcAnv/dHXEcrQAoW8ws5s5vo5n6bSk7k68D3S1qJwM38xat6GE.'}
]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        for index, dic in enumerate(USERS):
            model = MyModel(first_name=dic["first_name"],
                            last_name=dic["last_name"],
                            user_name=dic["user_name"],
                            email=dic["email"],
                            fav_food=dic["fav_food"],
                            password=dic["password"])
            dbsession.add(model)
