from uuid import uuid4

from django.contrib.postgres.indexes import BrinIndex
# / HashIndex / BTreeIndex
from django.db import models


def generate_uuid():
    return uuid4()


class UUIDMixin(models.Model):
    uuid = models.UUIDField(
        default=generate_uuid, verbose_name='UUID',
        editable=False, unique=True
    )

    class Meta:
        abstract = True
        indexes = (
            BrinIndex(fields=['uuid']),
            # HashIndex(fields=['uuid']),
            # BTreeIndex(fields=['uuid']),
        )  # Видел аргументы за все 3 индекса,
        # в текущей компании все в итоге сошлись на Брине
