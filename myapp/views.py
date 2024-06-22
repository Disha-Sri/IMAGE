from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image, ExifTags
from .serializers import ImageUploadSerializer

class ImageMetadataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            try:
                with Image.open(image) as img:
                    exif_data = img._getexif()
                    metadata = {
                        "Filename": img.filename,
                        "Image Size": img.size,
                        "Image Height": img.height,
                        "Image Width": img.width,
                        "Image Format": img.format,
                        "Image Mode": img.mode,
                        "Image is Animated": getattr(img, 'is_animated', False),
                        "Frames in Image": getattr(img, 'n_frames', 1),
                    }
                    
                    if exif_data:
                        exif = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}
                        metadata.update(exif)

                    return Response(metadata, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
