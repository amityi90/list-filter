import sqlalchemy
from sqlalchemy import text
from shapely.geometry import Polygon, LineString, Point, MultiPolygon
from shapely import wkb
import shapely
import geopandas
import datetime

before1 = datetime.datetime.now()

s = ('0106000020E6100000010000000103000000010000000A000000BAD81263F6ADE8BFD0767B634FD24440BECECCEE8AAEE8BF1528CA3C4CD24440919CC97EE9AFE8BF8AC3D8634ED24440E ... (74 characters truncated) ... 6E8BFA64CC1814BD24440C485FA811BABE8BFF9DE79346FD24440B824C13FE9A9E8BF001AB1DE6AD244409F21AAD735AFE8BF52C377B851D24440BAD81263F6ADE8BFD0767B634FD24440',)
print(s[0])

interns_conn = sqlalchemy.create_engine('postgresql://amit_m:Amit_2022!@10.0.1.4/interns_playground')
connection = interns_conn.connect()

metadata = sqlalchemy.MetaData()
table = sqlalchemy.Table('map_layers_spain_with_union', metadata, autoload=True, autoload_with=interns_conn)

# make multi-plygon from table

command = f"SELECT wkb_geometry FROM spain_fomento_server83_623192eb8ef943ed9897f8ade36945c0_0"
t = text(command)
result = connection.execute(t).fetchall()
print(type(result))
multi_polygons = []
for mp in result:
    multi_polygons.append(wkb.loads(mp[0], hex=True))
gs = geopandas.GeoSeries(multi_polygons)

unary_union_time = datetime.datetime.now()
nmp1 = gs.unary_union
now = datetime.datetime.now()
print('\n\n -----unary_union time: ', now - unary_union_time, '-----')
cascaded_union_time = datetime.datetime.now()
nmp2 = shapely.ops.cascaded_union(multi_polygons)
now = datetime.datetime.now()
print('\n\n -----cascaded_union time: ', now - cascaded_union_time, '-----')

# pushing the multi-polygon to multi-polygons table

pushing_new_row_time = datetime.datetime.now()
command = f"SELECT * FROM public.map_layers_spain WHERE table_name='spain_fomento_server83_623192eb8ef943ed9897f8ade36945c0_0';"
t = text(command)
result = connection.execute(t).fetchall()
print(result[0]._mapping)
row_to_insert = dict(result[0]._mapping)
row_to_insert['union_multipoligon'] = nmp1.wkb_hex
connection.execute(table.insert(), [row_to_insert])
now = datetime.datetime.now()
print('\n\n -----pushing_new_row time: ', now - pushing_new_row_time, '-----')

# query to the multi-polygon from multi-polygons table

before2 = datetime.datetime.now()

command = f"SELECT union_multipoligon FROM map_layers_spain_with_union WHERE NOT union_multipoligon='not yet' AND NOT union_multipoligon IS NULL;"
t = text(command)
result = connection.execute(t).fetchall()
# print(result[0][0])

mp = wkb.loads(result[0][0], hex=True)
# print(mp)

# calculate the intersection

bbox_polygon = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
s = geopandas.GeoSeries([bbox_polygon],)


before = datetime.datetime.now()
print(s.intersection(mp))
now = datetime.datetime.now()
print('\n\n -----time: ', now - before, '-----')
print('\n\n -----time with query: ', now - before2, '-----')
print('\n\n -----time with query: ', now - before1, '-----')


