import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True, null=True)
    modified = models.DateTimeField(_('modified'), auto_now=True, null=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
