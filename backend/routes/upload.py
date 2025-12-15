import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from server import db  # not used, but kept for consistency if needed
from auth.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

logger = logging.getLogger(__name__)

upload_router = APIRouter(prefix="/upload", tags=["upload"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def require_auth(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Não autorizado")
    return payload


@upload_router.post("/image")
async def upload_image(file: UploadFile = File(...), payload=Depends(require_auth)):
    """
    Faz upload de imagem para Cloudinary e retorna a URL.
    Requer envs:
      CLOUDINARY_CLOUD_NAME
      CLOUDINARY_API_KEY
      CLOUDINARY_API_SECRET
    """
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        raise HTTPException(status_code=500, detail="Cloudinary não configurado")

    try:
        import cloudinary
        import cloudinary.uploader
    except ImportError:
        raise HTTPException(status_code=500, detail="Dependência cloudinary ausente")

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )

    # Valida tipo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser imagem")

    try:
        result = cloudinary.uploader.upload(file.file, folder="financeia/uploads")
        url = result.get("secure_url")
        if not url:
            raise HTTPException(status_code=500, detail="Falha no upload")
        return {"url": url}
    except Exception as e:
        logger.error(f"Erro ao fazer upload: {e}")
        raise HTTPException(status_code=500, detail="Erro ao fazer upload")




