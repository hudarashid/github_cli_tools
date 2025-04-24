import os


class Config:
    GH_TOKEN = os.environ["GH_TOKEN"]
    GH_CONTENT_TYPE = os.environ["GH_CONTENT_TYPE"]
    GH_API_VERSION = os.environ["GH_API_VERSION"]
