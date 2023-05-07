# Global schema
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


# custom API response
class Response(GenericModel, Generic[T]):
    status: str
    message: str
    result: Optional[T]
