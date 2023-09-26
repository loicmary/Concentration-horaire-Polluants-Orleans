import pandas as pd
import json

def preprocessing(dataframe):
    """
    Returns a dataframe after operations on the features
    Args : dataframe (Pandas.dataframe) : data about pollution from https://www.data.gouv.fr/fr/datasets/concentration-horaire-des-polluants-air-ambiant-ligair-orleans-metropole/  
    """
    dataframe.drop(dataframe[dataframe['statut_valid'] == '0'].index, inplace = True)
    final_dataframe = dataframe[['nom_poll','date_debut','valeur','geo_shape','geo_point_2d','nom_com','nom_station']]
    final_dataframe.loc[:,"geo_shape"] = final_dataframe["geo_shape"].apply(json.loads)
    final_dataframe.loc[:,'longitude'] = final_dataframe['geo_shape'].apply(lambda x:x['coordinates'][0])
    final_dataframe.loc[:,'latitude'] = final_dataframe['geo_shape'].apply(lambda x:x['coordinates'][1])
    final_dataframe.loc[:,'date_debut'] = pd.to_datetime(final_dataframe.loc[:,'date_debut'], utc=False).dt.tz_localize(None)
    
    
    return final_dataframe.drop(columns=['geo_shape', 'geo_point_2d'], inplace=False)

def filtered_dataframe(dtf, month, day, hour, molecule, year=2023):
    """
    Returns a dataframe after some conditions on the features

    Args:
    dtf (Pandas.dataframe) : data about the pollution
    month (int) : the number of the month (from 1 to 12)
    day (int) : the number of the day (from 1 to 31)
    hour (int) : from 0 to 23
    molecule (str) : name of the molecule
    year (int) 
    """

    df = dtf[(dtf['date_debut'] == pd.Timestamp(year=year,month=month, day=day, hour=hour))
                   & (dtf['nom_poll']== molecule)]
    return df