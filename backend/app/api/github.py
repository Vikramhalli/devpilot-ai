from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.repository import Repository
from app.models.user import User
from app.schemas.repository import (
    RepositoryImportRequest,
    RepositoryResponse,
)
from app.services.github import get_repository


router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)


@router.post(
    "/import",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def import_repository(
    request: RepositoryImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    parsed_url = urlparse(str(request.github_url))

    if parsed_url.netloc.lower() != "github.com":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only GitHub repository URLs are supported",
        )

    parts = [
        part
        for part in parsed_url.path.strip("/").split("/")
        if part
    ]

    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GitHub repository URL",
        )

    owner, repo = parts

    if repo.endswith(".git"):
        repo = repo[:-4]

    try:
        github_data = get_repository(owner, repo)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub repository not found",
        )

    repository = Repository(
        name=github_data["name"],
        full_name=github_data["full_name"],
        owner=github_data["owner"]["login"],
        github_url=github_data["html_url"],
        clone_url=github_data["clone_url"],
        default_branch=github_data["default_branch"],
        language=github_data["language"],
        description=github_data["description"],
        imported_by=current_user.id,
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository