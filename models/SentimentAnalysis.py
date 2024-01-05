from fastapi import APIRouter
import pandas as pd

router = APIRouter() 

# rutas de los datos
output_steam_games = pd.read_parquet('Data/parquet/output_steam_games.parquet')
australian_user_reviews = pd.read_parquet('Data/parquet/australian_user_reviews.parquet')

class Analysis:
    @router.get('/')
    def sentiment_analysis(empresa_desarrolladora: str):
        games_developer = output_steam_games[output_steam_games['developer'] == empresa_desarrolladora]

        merge = pd.merge(games_developer, australian_user_reviews, left_on='id', right_on='item_id')

        sentiment_mapping = {
            0: 'Sentmiento Negativo',
            1: 'Sentimiento Neutral',
            2: 'Sentimiento Positovo'
        }
        sentiment = merge['sentiment_analysis'].map(sentiment_mapping).value_counts().to_dict()

        return {empresa_desarrolladora: sentiment}
    
analysis = Analysis()