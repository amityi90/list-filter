import sqlalchemy
from sqlalchemy import text
from shapely.geometry import Polygon, LineString, Point, MultiPolygon
from shapely import wkb
import shapely
import geopandas

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

interns_conn = sqlalchemy.create_engine('postgresql://amit_m:Amit_2022!@35.205.102.237/interns_playground')
connection = interns_conn.connect()

metadata = sqlalchemy.MetaData()
table = sqlalchemy.Table('map_layers_spain_with_union', metadata, autoload=True, autoload_with=interns_conn)

command = f"SELECT * FROM public.map_layers_spain WHERE table_name='spain_fomento_server83_623192eb8ef943ed9897f8ade36945c0_0';"
t = text(command)
result = connection.execute(t).fetchall()
print(result[0]._mapping)
row_to_insert = dict(result[0]._mapping)
row_to_insert['union_multipoligon'] = 'not yet'
connection.execute(table.insert(), [row_to_insert])

# tuple1 = str(result[0])[:-1] + ", 'not_yet')"
# print(tuple1)
# row = str(tuple1)

# # command = """CREATE TABLE IF NOT EXISTS map_layers_spain_with_union
# #     (
# #         id integer,
# #         layer_name text,
# #         table_name text,
# #         title_es text,
# #         id_column text,
# #         geometry_column text,
# #         default_columns text,
# #         layer_type text,
# #         height_column text,
# #         height_column_to_compare text,
# #         visible_on_first_load boolean,
# #         is_independent boolean,
# #         id_column_gush text,
# #         layer_to_compare text,
# #         legend_col text,
# #         exclude_flag boolean,
# #         layer_to_compare_geom_col text,
# #         col_to_ignore text,
# #         val_to_ignore text,
# #         city_id integer,
# #         firstmap boolean,
# #         secondmap boolean,
# #         enable boolean,
# #         title_en text,
# #         distance text,
# #         secondmap_after_purchase boolean,
# #         apply_country boolean,
# #         prov_ids text,
# #         permission text,
# #         lock_color boolean
# #     )"""

# # t = text(command)
# # result = connection.execute(t)

# # command = "ALTER TABLE map_layers_spain_with_union ADD union_multipoligon text;"

# # t = text(command)
# # result = connection.execute(t)

# command = f"INSERT INTO map_layers_spain_with_union(id, layer_name, table_name, title_es, id_column, geometry_column, default_columns, layer_type, height_column, height_column_to_compare, visible_on_first_load, is_independent, id_column_gush, layer_to_compare, legend_col, exclude_flag, layer_to_compare_geom_col, col_to_ignore, val_to_ignore, city_id, firstmap, secondmap, enable, title_en, distance, secondmap_after_purchase, apply_country, prov_ids, permission, lock_color, union_multipoligon) VALUES {row};"

# t = text(command)
# result = connection.execute(t)


