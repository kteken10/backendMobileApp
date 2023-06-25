from sqlalchemy import create_engine, MetaData

# URL de la base de données PostgreSQL
db_url = "postgresql://rodgxvok:o0UXFO3rc5bdFmU0rb_ptBSXAhneDQaS@silly.db.elephantsql.com/rodgxvok"

# Création d'un moteur SQLAlchemy
engine = create_engine(db_url)

# Création d'un objet MetaData
metadata = MetaData()

# Chargement des métadonnées existantes de la base de données
metadata.reflect(bind=engine)

# Suppression de toutes les tables
metadata.drop_all(bind=engine)

print("Toutes les tables ont été supprimées avec succès.")
