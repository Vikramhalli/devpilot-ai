from pydantic import BaseModel, HttpUrl


class RepositoryImportRequest(BaseModel):
    github_url: HttpUrl


class RepositoryResponse(BaseModel):
    id: int
    name: str
    full_name: str
    owner: str
    github_url: str
    clone_url: str
    default_branch: str
    language: str | None
    description: str | None
    imported_by: int

    model_config = {
        "from_attributes": True
    }