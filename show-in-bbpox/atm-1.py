import pandas as pd
import json

def getColor_v3(country:str, layerIdArr:str, chosenLang:str, point_arr:Optional[str]= '' ):
	connection= getattr(database, "%s_conn" % country.lower())
	s = text(
		"SELECT map_layers.id, map_layers_color.color, map_layers_color.title, map_layers.layer_type, map_layers.id_column, map_layers.visible_on_first_load, map_layers.is_independent, map_layers.title_"+str(chosenLang)+" as layer_title, map_layers.legend_col, map_layers.distance FROM map_layers_color INNER JOIN map_layers ON map_layers_color.layer_ref = map_layers.id AND map_layers.id = ANY(ARRAY["+str(layerIdArr)+"])")
	results = connection.execute(s).fetchall()
	if (len(results) > 0):
		if point_arr != '':
			df = pd.DataFrame(json.loads(json.dumps(results)))
			df_clean = df.drop_duplicates(subset=['id'])
			df_to_check = df_clean.loc[(df_clean['distance'].notna()) & (~df_clean['legend_col'].isnull())]
			if len(df_to_check) > 0:
				point_arr = point_arr.split(",")
				for index, row in df_to_check.iterrows():
					s1 = text(
					"SELECT snapland_plan_in_area(" + str(row['id']) +",ARRAY "+str(point_arr)+" )")
					results2 = connection.execute(s1).fetchall()
					filtered = filter(lambda res: (res['id'] != row["id"]) or ((res['id'] == row["id"]) and (res['title'] in (results2[0][0]))), results)
					results = list(filtered)
		return results
	else:
		return ''