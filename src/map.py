import pandas as pd
import numpy as np
import geopandas as gpd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import toml
import matplotlib.pyplot as plt
import plotly.express as px

try:
    pdf_table01 = pd.read_csv(r"..\csv\00-tabla-hogares-Encuesta de Niveles de Vida 2003.csv")
    pdf_map_cord = pd.read_csv(r"..\pan_coord.csv")
    pdf_merge = pdf_table01.merge(pdf_map_cord, left_on="lugar", right_on="Province", how="left")
    pdf_merge.drop(labels="Province", axis=1, inplace=True)

    # Convert the "lat" and "long" columns to geometry points
    # pdf_merge["geometry"] = pdf_merge.apply(lambda row: row if np.isnan(row["lat"]) else gpd.points_from_xy(row["long"], row["lat"]), axis=1)
    # pdf_merge["geometry"] = pdf_merge.apply(
    #     lambda row: gpd.points_from_xy(row["long"], row["lat"]) if not pd.notnull(row["lat"]) and not pd.notnull(row["long"]) else np.nan,
    #     axis=1
    # )

    geometry = gpd.points_from_xy(pdf_merge["lat"], pdf_merge["long"])
    pdf_merge["geometry"] = geometry
    # pdf_merge.to_csv("tabla01.csv")
    # Convert the dataframe to a GeoDataFrame
    gdf = gpd.GeoDataFrame(pdf_merge, geometry="geometry", crs="epsg:4326")

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

    pdf_info = pdf_table01.merge(pdf_map_cord, left_on="lugar", right_on="Province")
    geom = gpd.points_from_xy(pdf_info["long"], pdf_info["lat"])
    pdf_info["geometry"] = geom
    pdf_info = pdf_info.merge(gdf_map, left_on="lugar", right_on="nombre")
    pdf_info.drop(labels=["geom","nombre","tipo", "Province"], inplace=True, axis=1)

    gdf_info = gpd.GeoDataFrame(data=pdf_info,geometry="geometry",crs=4326)
    # graficar un mapa sobre el otro
    # fig, ax = plt.subplots(figsize=(10, 10))
    # gdf_map.plot(cmap="magma", column='nombre', linewidth=2, facecolor="black", ax=ax)
    # gdf_info.plot(ax=ax, cmap='viridis')

    #plotly
    # pan, ax = plt.subplots(figsize=(10,10),subplot_kw=dict(aspect="equal"))

    # pan = px.choropleth(pdf_info,
    #                     locations="pk",
    #                     geojson=gdf_map,
    #                     color="Muestra_Expandida",
    #                     title="Encuesta niveles de vida",
    #                     color_continuous_scale=px.colors.sequential.Plasma,
    #                     hover_name="lugar",
    #                     hover_data=["Muestra1"],
    #                     labels={"datos de muestra": "porcentaje"},
    #                     scope="north america")

    pan = px.choropleth_mapbox(
                    pdf_info,
                    locations="pk",
                    geojson=gdf_map,
                    color="Muestra1",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Encuesta de niveles de vida, 2003",
                    labels={"datos de muestra": "porcentaje"},
                    hover_name="lugar",
                    hover_data=["Muestra1","Muestra2"],
                    mapbox_style="open-street-map",
                    zoom=3,
                    opacity=0.5,
                    center={'lat': 8.5380, 'lon': -80.7821},
                    )
    pan.update_geos(fitbounds="locations",visible=False)
    pan.show()
    # fig.show()
    print("success")


except Exception as e:
    print(f"el error esta en : {e}")

