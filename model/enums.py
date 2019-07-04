import enum


class DType(enum.Enum):
    Int = "I"
    Long = "L"
    Float = "F"
    String = "S"
    Byte = "B"
    Image = "M"

class ImageFormat(enum.Enum):
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    TIFF = "tiff"
    BMP = "bmp"
    BAT = "bat"
    RAW = "raw"

