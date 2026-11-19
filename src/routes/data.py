from fastapi import FastAPI, APIRouter ,Depends, UploadFile ,status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings ,Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
import logging
from .schemes.data import ProcessRequest

logger = logging.getLogger("uvicorn.error")

data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api/v1","data"]
)
@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile ,app_settings : Settings =Depends(get_settings)):
    
   data_controller=DataController()
   is_valid,result_signal=data_controller.validate_uploaded_file(file=file)
   
   if not is_valid:
       return JSONResponse(
           status_code=status.HTTP_400_BAD_REQUEST,
           content={"signal": result_signal, "valid": is_valid}
   
    )
  
   
   project_dir_path=ProjectController().get_project_path(project_id=project_id)
   file_path,file_id=data_controller.generate_unique_filepath(original_file_name=file.filename,project_id=project_id)
   try: 
      async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):  # Read the file in chunks
            await f.write(chunk)   
   except Exception as e:
        logger.error(f"error while uploading file :  {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value,
                     "valid": False}
        )
   return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"signal": result_signal, 
                     "valid": is_valid, 
                     "file_id": file_id,
                     }
            
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    file_chunks=process_controller.process_file_content(file_id=file_id,
                                                        file_content=file_content,
                                                        chunk_size=chunk_size,
                                                        chunk_overlap=overlap_size
                                                    )
    if chunk_size is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value,
                     "valid": False}
        )
    return file_chunks
