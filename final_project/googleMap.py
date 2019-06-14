import urllib.request
from PIL import Image,ImageTk
import io

ZOOM_LEVEL_1,ZOOM_LEVEL_2,ZOOM_LEVEL_3,ZOOM_LEVEL_4,ZOOM_LEVEL_5 = range(5)

SCALE_RATIO = [(5750,7625),(11500,15250),(23000,30500),(46000,6100),(46000,61000)]


def GetImageFromURL(url):
    u = urllib.request.urlopen(url)
    raw_data = u.read()
    im = Image.open(io.BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    u.close()
    return image

class GoogleMap:
    def __init__(self):
        self.Latitude = None
        self.Longitude = None
        self.MapType = None
        self.Zoom = None
        self.Size = "400x400"
        self.coordX,self.coordY = 0,0
        self.image = None

    def UpdateMapImage(self):
        global Latitude,Longitude,MapType,Zoom,size

        key = 'AIzaSyAUb4eSn53l2uZd9QqpZjvB37ClazLfRgY'
        baseURL = 'https://maps.googleapis.com/maps/api/staticmap?center=LATITUDE,LONGITUDE&zoom=ZOOM&size=SIZE&maptype=MAP_TYPE&key='
        URL = baseURL + key

        URL = URL.replace("LATITUDE", self.Latitude)
        URL = URL.replace("LONGITUDE", self.Longitude)
        URL = URL.replace("MAP_TYPE", self.MapType)
        URL = URL.replace("ZOOM", str(self.Zoom+13))
        URL = URL.replace("SIZE", self.Size)
        self.image = GetImageFromURL(URL)

    def StartMap(self,Latitude,Longitude,MapType='roadmap',Zoom=ZOOM_LEVEL_3):
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.MapType = MapType
        self.Zoom = Zoom
        self.UpdateMapImage()

    def click(self, event):
        self.coordX,self.coordY = event.x, event.y

    def drag(self, x,y):
        self.move(self.coordX - x, self.coordY - y)
        self.coordX,self.coordY = x, y
        self.UpdateMapImage()

    def move(self,deltaX,deltaY):

        self.Latitude = str(float(self.Latitude) - deltaY/SCALE_RATIO[self.Zoom][1])
        self.Longitude = str(float(self.Longitude) + deltaX/SCALE_RATIO[self.Zoom][0])

    def GetMapImage(self):
        return self.image

    def ZoomIn(self):
        self.Zoom = min(self.Zoom+1,4)

    def ZoomOut(self):
        self.Zoom = max(self.Zoom-1, 0)