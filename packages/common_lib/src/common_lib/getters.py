import uuid

from common_lib.schemas import Event


def get_random_event() -> Event:
    return Event(
        id=str(uuid.uuid4()),
        name=str(uuid.uuid4()),
        description=f"Random event {uuid.uuid4()}",
    )
