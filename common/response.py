from decimal import Decimal
from django.db.models.fields.files import FieldFile, ImageField
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.conf import settings
import json
import datetime
from .utils.jsonutil import dumps
from .utils.strutil import camel
import base64


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FieldFile) or isinstance(obj, ImageField):
            if obj != '' and hasattr(obj, 'url'):
                return {'url': obj.url, 'name': obj.name, 'file': obj.name}
            else:
                return {}
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime.date):
            return datetime.date.strftime(obj, '%Y-%m-%d')
        if isinstance(obj, datetime.time):
            return datetime.time.strftime(obj, '%H:%M:%S')
        if isinstance(obj, datetime.timedelta):
            return str(obj)
        return super(MyEncoder, self).default(obj)


def serialize(query_set, relations=None, properties=None):
    if relations is None:
        relations = []
    if properties is None:
        properties = []
    if query_set is None:
        return None
    if isinstance(query_set, dict):
        return query_set

    if isinstance(query_set, QuerySet) or isinstance(query_set, list):
        data = []

        for qs in query_set:
            one_row = dict()
            rels = relations.copy()
            for col in qs._meta.get_fields():
                if col.is_relation:
                    if col.name not in rels:
                        continue
                    rels.remove(col.name)
                    if col.one_to_one or col.many_to_one:
                        one_row[camel(col.name)] = serialize(getattr(qs, col.name, None), rels, properties)
                    else:
                        one_row[camel(col.name)] = serialize(getattr(qs, col.name).all(), rels, properties)
                else:
                    one_row[camel(col.name)] = getattr(qs, col.name)
            for prop in properties:
                try:
                    one_row[camel(prop)] = getattr(qs, prop)
                except:
                    pass

            data.append(one_row)
    else:
        data = dict()
        rels = relations.copy()
        for col in query_set._meta.get_fields():
            if col.is_relation:
                if col.name not in rels:
                    continue
                rels.remove(col.name)
                if col.one_to_one or col.many_to_one:
                    data[camel(col.name)] = serialize(getattr(query_set, col.name, None), rels, properties)
                else:
                    data[camel(col.name)] = serialize(getattr(query_set, col.name).all(), rels, properties)
            else:
                data[camel(col.name)] = getattr(query_set, col.name)
        for prop in properties:
            try:
                data[camel(prop)] = getattr(query_set, prop)
            except:
                pass

    return data


def str_to_base64(s):
    if isinstance(s, bytes):
        return base64.b64encode(s).decode()
    else:
        return base64.b64encode(s.encode()).decode()


def base64_to_str(s):
    return base64.b64decode(s).decode()


def success(data=None):
    if data is None:
        data = []
    res = dict()
    res['code'] = '00'
    res['message'] = '请求成功!'
    res['data'] = data

    if settings.SECRET_MODE:
        src = dumps(res, cls=MyEncoder)
        res = {'body': str_to_base64(src)}
    return JsonResponse(res, encoder=MyEncoder)


def error(code='01', msg='', data=None):
    if data is None:
        data = {}
    res = dict()
    res['code'] = code
    res['message'] = msg
    res['data'] = data
    return JsonResponse(res, encoder=MyEncoder)
