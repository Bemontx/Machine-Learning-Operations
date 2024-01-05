from fastapi import APIRouter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

# rutas de los datos
output_steam_games = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/output_steam_games.parquet')

class GameRecommend:
    @router.get('/')
    def games_recommend(product_id: str):
        if product_id not in output_steam_games['id'].values:
            return {'error': 'ID de juego no encontrado'}

        selected_game = output_steam_games[output_steam_games['id'] == product_id]
        selected_game_features = selected_game['genres'].iloc[0] + ' ' + selected_game['tags'].iloc[0]

        all_games_features = output_steam_games['genres'] + ' ' + output_steam_games['tags']

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_games_features)

        cosine_sim = cosine_similarity(tfidf_vectorizer.transform([selected_game_features]), tfidf_matrix)
        game_scores = list(enumerate(cosine_sim[0]))

        similar_games = sorted(game_scores, key=lambda x: x[1], reverse=True)[1:6]

        recommended_games = [{'id': output_steam_games.iloc[i[0]]['id'], 'title': output_steam_games.iloc[i[0]]['title']} for i in similar_games if i[0] < len(output_steam_games)]

        return {'recommended_games': recommended_games}

gamesRecommend = GameRecommend()

