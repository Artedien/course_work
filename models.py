from sqlalchemy import Column, Integer, String, Float

from database import Base, engine



class ozon_base(Base):
    __tablename__ = 'ozon'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    model = Column(String())
    link = Column(String())
    price = Column(String())
    

    def __repr__(self):
        return f'Ozon{self.id}, {self.name}, {self.price}, {self.link},{self.model}'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)