from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from .schemas import AuthorCreateBase, AuthorUpdateBase, AuthorViewBase
from .filters import AuthorFilter
from .service import AuthorService


router = APIRouter()


@cbv(router)
class APIClass:

	db: AsyncSession = Depends(get_db)

	@router.post(path="/author/", response_model=AuthorViewBase, status_code=status.HTTP_201_CREATED)
	async def create_author(
							self,
							data: AuthorCreateBase):
		service = AuthorService(self.db)
		return await service.author_create(data)


	@router.put(path="/author/{id}/", response_model=AuthorViewBase, status_code=status.HTTP_200_OK)
	async def update_author(
							self,
							id: int,
							data: AuthorUpdateBase):
		service = AuthorService(self.db)
		return await service.author_update(id, data)


	@router.delete(path="/author/{id}/", status_code=status.HTTP_204_NO_CONTENT)
	async def delete_author(
							self,
							id: int):
		service = AuthorService(self.db)
		return await service.author_delete(id)


	@router.get(path="/author/{id}/", response_model=AuthorViewBase, status_code=status.HTTP_200_OK)
	async def get_author(
							self,
							id: int):
		service = AuthorService(self.db)
		return await service.author_retrieve(id)


	@router.get(path="/author/", response_model=list[AuthorViewBase], status_code=status.HTTP_200_OK)
	async def list_author(
							self,
							filter: AuthorFilter = FilterDepends(AuthorFilter)):
		service = AuthorService(self.db)
		return await service.author_list(filter)


@router.get(path="/middleware/")
async def middleware():
	return JSONResponse(content={"message": "Middleware is working"}, status_code=status.HTTP_200_OK)
