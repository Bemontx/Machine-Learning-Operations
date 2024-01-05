from fastapi import APIRouter
import pandas as pd

router = APIRouter()

#rutas de los datos
output_steam_games = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/output_steam_games.parquet')
australian_user_reviews = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/australian_user_reviews.parquet')

class Recommend:
    @router.get('/')
    def UsersRecommend(año: int):
        year_reviews = australian_user_reviews[australian_user_reviews['new_posted'].dt.year == año]
        positive_reviews = year_reviews[year_reviews['recommend'] == True]
        neutral_reviews = year_reviews[year_reviews['sentiment_analysis'].isin([0, 1])]  
        
        combined_reviews = pd.concat([positive_reviews, neutral_reviews])
        
        # Contar la cantidad de recomendaciones por juego
        games_recommendation_count = combined_reviews['item_id'].value_counts().reset_index()
        games_recommendation_count.columns = ['item_id', 'recommendation_count']
        
        # Convertir 'item_id' a tipo objeto para coincidir con el tipo en output_steam_games
        games_recommendation_count['item_id'] = games_recommendation_count['item_id'].astype(str)
        games_recommendation_count = pd.merge(games_recommendation_count, output_steam_games[['id', 'title']], left_on='item_id', right_on='id')
        
        top_3_games = games_recommendation_count.nlargest(3, 'recommendation_count')
        
        top_3_formatted = [{"Puesto 1": top_3_games.iloc[0]['title']},
                        {"Puesto 2": top_3_games.iloc[1]['title']},
                        {"Puesto 3": top_3_games.iloc[2]['title']}]
        
        return top_3_formatted



recommend = Recommend()
