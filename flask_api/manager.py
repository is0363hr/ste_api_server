from application import app, Base, ENGINE, manager
from flask_script import Server, Command
from www import *

from apscheduler_img import Map_update

# web server
manager.add_command(
    "runserver", Server(host="0.0.0.0", use_debugger=True, use_reloader=True)
)

# map = Map_update()
# map.sche_second_set(10)
# map.sche_start()

# create tables
@Command
def create_all():
    from common.models.cloud import Cloud

    Base.metadata.create_all(bind=ENGINE)


manager.add_command("create_all", create_all)


def main():
    manager.run()


if __name__ == "__main__":
    # app.run( host = "0.0.0.0" )

    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()