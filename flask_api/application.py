from flask import Flask
from flask_script import Manager
import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from config.local_setting import DATABASE_URI


app = Flask(__name__)

manager = Manager(app)
# app.config.from_pyfile("config/base_setting.py")
app.config.from_pyfile("config/local_setting.py")

# linux export ops_config=local|production
# windows set ops_config=local|production
if "ops_config" in os.environ:
    app.config.from_pyfile("config/%s_setting.py" % (os.environ["ops_config"]))


ENGINE = create_engine(
    DATABASE_URI, encoding="utf-8", echo=True
)  # Trueだと実行のたびにSQLが出力される
# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()