import sqlalchemy
from sqlalchemy import text
from shapely.geometry import Polygon, LineString, Point, MultiPolygon
from shapely import wkb
import shapely
import geopandas
import datetime
from decouple import config


interns_conn = sqlalchemy.create_engine(config('DB_CONNECTION_STRING'))
connection = interns_conn.connect()
metadata = sqlalchemy.MetaData()

class MP:
    def __init__(self, layer_table_name):
        self.layer_table_name = layer_table_name
        self.multi_polygons_table = sqlalchemy.Table(config('LAYERS_MULTIPOLYGONS_TABLE'), metadata, autoload=True, autoload_with=interns_conn)


    # make multi-plygon from table
    def creat_layer_multi_polygon(self):
        command = f"SELECT {config('GEOMETRY_COLUMN')} FROM {self.table_name}"
        text_command = text(command)
        result_layer_geometries = connection.execute(text_command).fetchall()
        layer_geometries = []
        for geometry in result_layer_geometries:
            layer_geometries.append(wkb.loads(geometry[0], hex=True))
        gs = geopandas.GeoSeries(layer_geometries)
        self.layer_main_multi_poligon_to_push = gs.unary_union

    # pushing the multi-polygon to multi-polygons table  !!!!!!!!!!!! TODO check if smaller table will be faster
    def push_main_multi_poligon_to_table(self):
        command = f"SELECT * FROM public.map_layers_spain WHERE table_name={self.layer_table_name};"
        text_command = text(command)
        result_layer_info = connection.execute(text_command).fetchall()
        row_to_insert = dict(result_layer_info[0]._mapping)
        row_to_insert['union_multipoligon'] = self.layer_main_multi_poligon_to_push.wkb_hex
        connection.execute(self.multi_polygons_table.insert(), [row_to_insert])

    # query to the multi-polygon from multi-polygons table 
    # TODO add bbox_polygon parameter, modify the SELECT command
    def make_intersectin(self):
        command = f"SELECT union_multipoligon FROM map_layers_spain_with_union WHERE NOT union_multipoligon='not yet' AND NOT union_multipoligon IS NULL;"
        t = text(command)
        result = connection.execute(t).fetchall()
        layer_multi_poligon = wkb.loads(result[0][0], hex=True)
        # calculate the intersection
        bbox_polygon = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
        bbox_series = geopandas.GeoSeries([bbox_polygon],)
        before = datetime.datetime.now()
        print(bbox_series.intersection(layer_multi_poligon))
        now = datetime.datetime.now()
        print('\n\n ----- intersection time: ', now - before, '-----')



new_mp = MP('spain_fomento_server83_623192eb8ef943ed9897f8ade36945c0_0')
new_mp.make_intersectin()