from fastapi import APIRouter
import pandas as pd

router = APIRouter()

# rutas de los datos
output_steam_games = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/output_steam_games.parquet')
australian_user_reviews = pd.read_parquet('/home/bemontx/Escritorio/app/Data/parquet/australian_user_reviews.parquet')

class Developer:
    @router.get('/')
    def UsersWorstDeveloper(año: int):

        negative_reviews = australian_user_reviews[
            (australian_user_reviews['new_posted'].dt.year == año) &
            (australian_user_reviews['recommend'] == False)
        ]

        merged_data = pd.merge(negative_reviews, output_steam_games[['id', 'developer']], left_on='item_id', right_on='id')

        developer_count = merged_data['developer'].value_counts()
        top_3_worst_developers = developer_count.nsmallest(3)

        top_3_formatted = [{"Puesto " + str(i + 1): developer} for i, developer in enumerate(top_3_worst_developers.index)]

        return top_3_formatted

developer = Developer()