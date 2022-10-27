import sqlalchemy
from sqlalchemy import text
from shapely.geometry import Polygon, LineString, Point, MultiPolygon
from shapely import wkb
import shapely
import geopandas
import datetime

s = ('0106000020E6100000010000000103000000010000000A000000BAD81263F6ADE8BFD0767B634FD24440BECECCEE8AAEE8BF1528CA3C4CD24440919CC97EE9AFE8BF8AC3D8634ED24440E ... (74 characters truncated) ... 6E8BFA64CC1814BD24440C485FA811BABE8BFF9DE79346FD24440B824C13FE9A9E8BF001AB1DE6AD244409F21AAD735AFE8BF52C377B851D24440BAD81263F6ADE8BFD0767B634FD24440',)
print(s[0])

interns_conn = sqlalchemy.create_engine('postgresql://amit_m:Amit_2022!@35.205.102.237/interns_playground')
connection = interns_conn.connect()

metadata = sqlalchemy.MetaData()
table = sqlalchemy.Table('map_layers_spain_with_union', metadata, autoload=True, autoload_with=interns_conn)

# command = f"SELECT wkb_geometry FROM spain_fomento_server83_623192eb8ef943ed9897f8ade36945c0_0"
# t = text(command)
# result = connection.execute(t).fetchall()
# print(type(result))
# multi_polygons = []
# for mp in result:
#     multi_polygons.append(wkb.loads(mp[0], hex=True))
# gs = geopandas.GeoSeries(multi_polygons)
# nmp1 = gs.unary_union
# # print(nmp1)
# # nmp2 = shapely.ops.cascaded_union(multi_polygons)
# # print(nmp2)

# command = f"SELECT * FROM public.map_layers_spain WHERE table_name='spain_fomento_server83_623192eb8ef943ed9897f8ade36945c0_0';"
# t = text(command)
# result = connection.execute(t).fetchall()
# print(result[0]._mapping)
# row_to_insert = dict(result[0]._mapping)
# row_to_insert['union_multipoligon'] = nmp1.wkb_hex
# connection.execute(table.insert(), [row_to_insert])
before1 = datetime.datetime.now()

command = f"SELECT union_multipoligon FROM map_layers_spain_with_union WHERE NOT union_multipoligon='not yet' AND NOT union_multipoligon IS NULL;"
t = text(command)
result = connection.execute(t).fetchall()
# print(result[0][0])

mp = wkb.loads(result[0][0], hex=True)
# print(mp)

bbox_polygon = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
s = geopandas.GeoSeries([bbox_polygon],)


before = datetime.datetime.now()
print(s.intersection(mp))
now = datetime.datetime.now()
print('\n\n -----time: ', now - before, '-----')
print('\n\n -----time with query: ', now - before1, '-----')


