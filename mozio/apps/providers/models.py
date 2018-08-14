import re
import uuid

from django.db import models
from django.core.exceptions import ValidationError

def emailValidator(val):
    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', val)
    if match == None:
	    raise ValidationError('input is not an email')


def phoneNumberValidator(val):
    match = re.match(
        '^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)'
        '?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$',
        val
    )
    if match == None:
        raise ValidationError('input is not a phone number')


# NOTE: indexes are not created! That requires more information about how the
# API would be used.
class Provider(models.Model):
    # a unique id of this provider
    Id = models.CharField(primary_key=True, max_length=96, unique=True, default=uuid.uuid4)

    # any string will do here
    Name = models.CharField(max_length=1024)

    # this field contains a very basic email validator
    Email = models.CharField(max_length=2048, validators=(emailValidator,))

    # must be numbers only!
    PhoneNumber = models.CharField(max_length=32, validators=(phoneNumberValidator,))

    # expected locale names: 'en-us', 'en-au', 'de'
    Language = models.CharField(max_length=16)

    # expected extended currency names: 'BAM', 'USD' etc
    Currency = models.CharField(max_length=16)

    def __str__(self):
        return '{} > {} {}'.format(self.Id, self.Name, self.Email)

    def to_dict(self):
        return {
            'id': self.Id,
            'name': self.Name,
            'email': self.Email,
            'phone_number': self.PhoneNumber,
            'language': self.Language,
            'currency': self.Currency
        }

