from fastapi import FastAPI
import pandas as pd

#importamos nuestros router de nuestra carpeta models
from models.PlayTimeGenre import router as PlayTimeGenre
from models.UserForGenre import router as UserForGenre
from models.UsersRecommend import router as UsersRecommend
from models.UsersWorstDeveloper import router as UsersWorstDeveloper
from models.SentimentAnalysis import router as SentimentAnalysis
from models.GamesRecommend import router as GamesRecommend

app = FastAPI()

# rutas de los datos
output_steam_games = pd.read_parquet('Data/parquet/output_steam_games.parquet')
australian_user_reviews = pd.read_parquet('Data/parquet/australian_user_reviews.parquet')
australian_users_items = pd.read_parquet('Data/parquet/output_steam_games.parquet')

# instanciamos nuestros router
app.include_router(PlayTimeGenre, prefix="/PlayTimeGenre", tags=['PlayTimeGenre'])
app.include_router(UserForGenre, prefix="/UserForGenre", tags=['UserForGenre'])
app.include_router(UsersRecommend, prefix="/UsersRecommend", tags=['UsersRecommend'])
app.include_router(UsersWorstDeveloper, prefix="/UsersWorstDeveloper", tags=['UsersWorstDeveloper'])
app.include_router(SentimentAnalysis, prefix="/SentimentAnalysis", tags=['SentimentAnalysis'])
app.include_router(GamesRecommend, prefix="/GamesRecommend", tags=['GamesRecommend'])