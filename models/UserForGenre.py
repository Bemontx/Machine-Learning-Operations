from fastapi import APIRouter
import pandas as pd

router = APIRouter()

#rutas de los datos
output_steam_games = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/output_steam_games.parquet')
australian_users_items = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/australian_users_items.parquet')

class Users:
    @router.get('/')
    def UserForGenre(genero):
        genre_data = output_steam_games[output_steam_games['genres'].str.contains(genero, case=False)]
        
        if genre_data.empty:
            return f"No hay datos de horas jugadas para el género {genero}"
        
        merged_data = pd.merge(genre_data, australian_users_items, left_on='id', right_on='item_id', how='inner')
        
        # Convertir la columna release_date al formato de fecha apropiado
        merged_data['release_date'] = pd.to_datetime(merged_data['release_date'], errors='coerce')
        
        # Filtrar las filas con fechas válidas
        merged_data = merged_data.dropna(subset=['release_date'])
        
        if merged_data.empty:
            return f"No hay datos de horas jugadas para el género {genero}"
        
        user_hours_per_year = merged_data.groupby(['steam_id', merged_data['release_date'].dt.year])['playtime_forever'].sum().reset_index()
        
        if user_hours_per_year.empty:
            return f"No hay datos de horas jugadas para el género {genero}"
        
        user_most_played = user_hours_per_year.groupby('steam_id')['playtime_forever'].sum().idxmax()
        user_most_played_hours = user_hours_per_year[user_hours_per_year['steam_id'] == user_most_played]
        
        horas_por_anio = [{"Año": year, "Horas": hours} for year, hours in user_most_played_hours.set_index('release_date').to_dict()['playtime_forever'].items()]
        
        result = {
            "Usuario con más horas jugadas para Género": str(user_most_played),
            "Horas jugadas": horas_por_anio
        }
        
        return result
    
user = Users()