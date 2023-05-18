import pandas as pd
import numpy as np
import geopandas as gpd


pdf_table01 = pd.read_csv(r"..\csv\00-tabla-hogares-Encuesta de Niveles de Vida 2003.csv")
pdf_map_cord = pd.read_csv(r"..\pan_coord.csv")
pdf_merge = pdf_table01.merge(pdf_map_cord,left_on="lugar", right_on="Province", how="left")
pdf_merge.drop(labels="Province", axis=1, inplace=True)

# Convert the "lat" and "long" columns to geometry points
# pdf_merge["geometry"] = pdf_merge.apply(lambda row: row if np.isnan(row["lat"]) else gpd.points_from_xy(row["long"], row["lat"]), axis=1)
# pdf_merge["geometry"] = pdf_merge.apply(
#     lambda row: gpd.points_from_xy(row["long"], row["lat"]) if not pd.notnull(row["lat"]) and not pd.notnull(row["long"]) else np.nan,
#     axis=1
# )

geomtry = gpd.points_from_xy(pdf_merge["long"], pdf_merge["lat"])
pdf_merge["geometry"]=geomtry
pdf_info = pdf_table01.merge(pdf_map_cord, left_on="lugar", right_on="Province")
geom = gpd.points_from_xy(pdf_info["long"],pdf_info["lat"])
pdf_info["geometry"]=geom
pdf_info.drop(labels="Province",inplace=True, axis=1)
print("success")
