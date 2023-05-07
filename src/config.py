# global models
from .customers import models as CustomerModels
from .database import engine


# Create all models into target db
def createAllModels():
    # bind all models from different sources here
    CustomerModels.Base.metadata.create_all(bind=engine)

