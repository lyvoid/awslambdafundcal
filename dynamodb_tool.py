import boto3
import logging
from boto3.dynamodb.types import Decimal

_dynamodb = boto3.resource('dynamodb')
_tables = {}


class AssistColumnClass:
    pass


class TableMeta(type):

    def __new__(mcs, name, bases, attrs):
        if name == 'Table':
            return type.__new__(mcs, name, bases, attrs)

        # connect table to attrs['table']
        table_name = attrs.get('__table__', None) or name
        if table_name not in _tables:
            _tables[table_name] = _dynamodb.Table(table_name)
        attrs['__table__'] = _tables[table_name]

        # delete all assist attr
        tmp = []
        for k, v in attrs.items():
            if isinstance(v, AssistColumnClass):
                tmp.append(k)
        for k in tmp:
            attrs.pop(k)

        return type.__new__(mcs, name, bases, attrs)


class Table(metaclass=TableMeta):

    def __init__(self):
        self._data = {}

    def __getattr__(self, key):
        if key.startswith('_'):
            return self.__dict__.get(key)
        return self._data.get(key)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
        else:
            if isinstance(value, float):
                value = Decimal(str(value))
            self._data[key] = value

    def load(self, date):
        self._data.clear()
        items = self.__table__.get_item(Key={'date': date}).get('Item')
        if items is None:
            logging.warning('can not load data at %s' % date)
            return False
        else:
            self._data = items
            return True

    def commit(self):
        if self.date is None:
            logging.warning('can not commit to dynamodb since date is None')
            return False

        self.__table__.put_item(Item=self._data)
        return True

    def delete(self):
        self.__table__.delete_item(Key={'date': self.date})
