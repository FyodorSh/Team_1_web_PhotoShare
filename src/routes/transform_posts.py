import io
import base64
from typing import List
from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import cloudinary
import qrcode
import qrcode.image.svg
import qrcode.image.base

from src.schemas_transform_posts import TransformImageModel, URLTransformImageResponse, SaveTransformImageModel, \
    TransformImageResponse
from src.database.connect import get_db
from src.services.transform_posts import create_list_transformation
import src.repository.transform_posts as rep_transform
from src.services.messages_templates import NOT_FOUND

router = APIRouter(prefix='/image/transform', tags=['Transform Image'])


@router.post('/{image_id}', response_model=URLTransformImageResponse, status_code=status.HTTP_200_OK)
async def transformation_for_image(image_id: int, body: TransformImageModel, db: Session = Depends(get_db)):
    image_url = await rep_transform.get_image_for_transform(image_id, db)  # 'PythonContactsApp/Irina'
    cloudinary.config(
        cloud_name='drilpksk7',
        api_key='326193329941471',
        api_secret='1YqMfm4NEIJApzklq_lEaolH7-I',
        secure=True
    )
    transform_list = create_list_transformation(body)
    print(transform_list)
    url = cloudinary.CloudinaryImage(image_url).build_url(transformation=transform_list)
    return {'url': url}


@router.post('/save/{image_id}', response_model=TransformImageResponse, status_code=status.HTTP_201_CREATED)
async def save_transform_image(image_id: int, body: SaveTransformImageModel, db: Session = Depends(get_db)):
    img = await rep_transform.set_transform_image(image_id, body.url, db)
    if img is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return {'data': img}


@router.post('/qrcode/{image_id}', status_code=status.HTTP_200_OK)
async def get_qrcode_for_transform_image_(image_id: int, db: Session = Depends(get_db)):
    # image_url = 'https://res.cloudinary.com/drilpksk7/image/upload/e_grayscale:100/v1/PythonContactsApp/Irina'
    image_url = await rep_transform.get_transform_image(image_id, db)
    qr = qrcode.make(image_url.photo_url)
    buf = io.BytesIO()
    qr.save(buf)
    qr_code = base64.b64encode(buf.getvalue()).decode('ascii')
    return qr_code


@router.get('/{image_id}', response_model=List[TransformImageResponse], status_code=status.HTTP_200_OK)
async def get_transformed_image(image_id: int, db: Session = Depends(get_db)):
    return await rep_transform.get_transform_image(image_id, db)


@router.get('/all/{image_id}', response_model=List[TransformImageResponse], status_code=status.HTTP_200_OK)
async def get_list_of_transformed_image(image_id: int, db: Session = Depends(get_db)):
    return await rep_transform.get_all_transform_images(image_id, db)
