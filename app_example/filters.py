from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from .models import AuthorModel


class AuthorFilter(Filter):

    name: Optional[str] = None
    pseudo: Optional[str] = None
    search: Optional[str] = None
    order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = AuthorModel
        search_model_fields = ["city"]
