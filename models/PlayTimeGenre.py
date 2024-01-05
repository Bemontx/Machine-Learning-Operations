from fastapi import APIRouter
import pandas as pd

router = APIRouter()

#rutas de los datos
output_steam_games = pd.read_parquet('Data/parquet/output_steam_games.parquet')
australian_users_items = pd.read_parquet('Data/parquet/output_steam_games.parquet')

merged_data = pd.concat([output_steam_games, australian_users_items], axis=1)
merged_data = merged_data.dropna(subset=['genres'])

class Games:
    @router.get('/')
    def PlayTimeGenre(genero: str):
        
        genre_data = merged_data[merged_data['genres'].str.contains(genero, case=False)]
        
        if genre_data.empty:
            return f"No se encontraron datos para el género {genero}"
        
        genre_data['release_date'] = genre_data['release_date'].astype(str)
        genre_data['release_year'] = genre_data['release_date'].str.extract(r'(\d{4})')
        genre_data = genre_data.dropna(subset=['release_year'])
        genre_data['release_year'] = genre_data['release_year'].astype(int)
        
        genre_hours_per_year = genre_data.groupby('release_year')['playtime_forever'].sum()        
        year_most_played = genre_hours_per_year.idxmax()
        
        return {f"Año de lanzamiento con más horas jugadas para el género {genero}": str(year_most_played)}

games = Games()
