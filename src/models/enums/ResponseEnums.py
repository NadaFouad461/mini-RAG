from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCCESS = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not Supported"
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit"
    FILE_UPLOADED_SUCCESS= "File uploaded successfully"
    FILE_UPLOAD_FAILED= "File upload failed"
    PROCESSING_FAILED= "File processing failed"
    PROCESSING_SUCCESS= "File processed successfully"
    