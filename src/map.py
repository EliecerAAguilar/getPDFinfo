import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import toml
import matplotlib.pyplot as plt
from shapely.errors import ShapelyDeprecationWarning
import warnings

# warning de shapely tipo de datos que ya no se usaran
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

try:
    table01 = pd.read_csv(
        r"..\csv\00-tabla-hogares-Encuesta de Niveles de Vida 2003.csv")

    pdf_table01 = pd.DataFrame(data=table01)

    pan_data = pd.read_csv(r"..\pan_coord.csv")
    pdf_map_cord = pd.DataFrame(data=pan_data)

    values = list(pdf_map_cord.Province)
    index = []

    for x in values:
        index.append([int(pdf_table01.index[pdf_table01['lugar'] == x].to_list()[0]),
                      int(pdf_map_cord.index[pdf_map_cord['Province'] == x].to_list()[0]), x])

    pdf_table01["lat"] = np.nan
    pdf_table01["long"] = np.nan

    for idx, val in enumerate(index):
        pdf_table01.at[val[0], 'lat'] = pdf_map_cord.at[val[1], 'lat']
        pdf_table01.at[val[0], 'long'] = pdf_map_cord.at[val[1], 'long']

    # Convert the "lat" and "lon" columns to geometry points
    pdf_table01["geometry"] = pdf_table01.apply(lambda row: Point(row["long"], row["lat"]), axis=1)
    pdf_table01.to_csv("tabla01.csv")
    # Convert the dataframe to a GeoDataFrame
    gdf = gpd.GeoDataFrame(pdf_table01, geometry=pdf_table01["geometry"], crs="epsg:4326")

    config = toml.load("conf.toml")
    pasw: str = config["dbms_conf"]["_pas"]
    user: str = config["dbms_conf"]["_user"]
    port: int = config["dbms_conf"]["_port"]
    db: str = config["dbms_conf"]["_db"]
    dbms: str = config["dbms_conf"]["_dbms"]
    controller: str = config["dbms_conf"]["_controller"]
    host: str = config["dbms_conf"]["_host"]

    engine = create_engine(f"{dbms}+{controller}://{user}:{quote_plus(pasw)}@{host}:{port}/{db}")

    sql = """select * from pan_map;"""
    gdf_map = gpd.read_postgis(sql=sql, con=engine, geom_col="geom", crs='epsg:4326')
    gdf_info = gdf.iloc[16:, 0:-3]

    # graficar un mapa sobre el otro
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_map = gdf_map.to_crs(epsg=4326)
    gdf_map.plot(cmap="magma", edgecolor='black', column='name_1', ax=ax)
    gdf = gdf.to_crs(epsg=4326)
    gdf.plot(ax=ax, cmap='viridis', edgecolor='black')
    plt.show()
    print("success")


except Exception as e:
    print(e.args)

