from application import Base
from sqlalchemy import Column, Integer, String, DateTime, BLOB


class Cloud(Base):
    __tablename__ = "cloud_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_name = Column(String(100), nullable=False)
    img_cloud_path = Column(String(50), nullable=False)
    img_sye_path = Column(String(50), nullable=False)
    img_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    tag = Column(String(50), nullable=False)
    zoom_level = Column(Integer, nullable=False)