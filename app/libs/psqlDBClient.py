# postgres db engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://trovendb:troven@trovenapi.smartinternz.com:5432/trovenBeta', echo=False)
# engine = create_engine('postgresql://postgres:myPassword@34.239.0.240:5432/koneqto', echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def engine_with_schema(schema_name):
#     engine = create_engine('postgresql://postgres:Vikasdefensics@localhost:5432/troventest', echo=True)
#     SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
#     engine.execute('SET search_path TO {}'.format(schema_name))
#     return engine

