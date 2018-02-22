from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json
from django.template import Library

register = Library()

#https://stackoverflow.com/a/32429429
import datetime
import decimal

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    elif isinstance(value, decimal.Decimal):
        return str(value)
    else:
        return value.__dict__
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object, default=json_default,
            sort_keys=True, ensure_ascii=False)

register.filter('jsonify', jsonify)
