from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.repository import Repository
from app.models.user import User
from app.services.github import (
    get_repository_contents,
    get_file_content,
)
from app.services.ai import analyze_code


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.get("")
def get_user_repositories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repositories = db.scalars(
        select(Repository)
        .where(
            Repository.imported_by == current_user.id
        )
        .order_by(
            Repository.created_at.desc()
        )
    ).all()

    return repositories


@router.get("/{repository_id}/files")
def get_repository_files(
    repository_id: int,
    path: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = db.scalar(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.imported_by == current_user.id,
        )
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    try:
        contents = get_repository_contents(
            repository.owner,
            repository.name,
            path,
            repository.default_branch,
        )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Could not retrieve repository contents",
        )

    return contents


@router.get("/{repository_id}/file")
def get_repository_file(
    repository_id: int,
    path: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = db.scalar(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.imported_by == current_user.id,
        )
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    try:
        file_data = get_file_content(
            repository.owner,
            repository.name,
            path,
            repository.default_branch,
        )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    if file_data.get("type") != "file":
        raise HTTPException(
            status_code=400,
            detail="The specified path is not a file",
        )

    return {
        "name": file_data["name"],
        "path": file_data["path"],
        "size": file_data["size"],
        "download_url": file_data["download_url"],
        "sha": file_data["sha"],
        "content": file_data.get("decoded_content"),
    }


@router.post("/{repository_id}/analyze")
def analyze_repository_file(
    repository_id: int,
    path: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = db.scalar(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.imported_by == current_user.id,
        )
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    try:
        file_data = get_file_content(
            repository.owner,
            repository.name,
            path,
            repository.default_branch,
        )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    if file_data.get("type") != "file":
        raise HTTPException(
            status_code=400,
            detail="The specified path is not a file",
        )

    code = file_data.get("decoded_content")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="File has no readable content",
        )

    try:
        analysis = analyze_code(code)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(exc)}",
        )

    return {
        "repository_id": repository.id,
        "file_name": file_data["name"],
        "file_path": file_data["path"],
        "analysis": analysis,
    }