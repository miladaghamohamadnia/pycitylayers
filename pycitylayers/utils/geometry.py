from shapely.geometry import Polygon, Point, box


class GeometryGQL:
    def __init__(self):
        pass
    
    def format_geom(self, coords, epsg=4326, geom_type='Polygon'):
        formatted_geom = {
                            "geometry": {
                                "type": geom_type,
                                "coordinates": coords,
                                "crs":{"type":"name","properties":{"name":f"EPSG:{epsg}"}}
                            }
                        }
        return formatted_geom
    
    
class PointGQL(GeometryGQL):
    def __init__(self):
        super().__init__()
        self.geom_type = "Point"
    
    def point(self, x, y):
        point = Point(x, y)
        point = [xy[0] for xy in point.coords.xy]
        return self.format_geom(point, geom_type=self.geom_type)
    
    
    
class PolygonGQL(GeometryGQL):
    def __init__(self):
        super().__init__()
        self.geom_type = "Polygon"
    
    def rect_from_two_corners(self, p1, p2):
        xmin = min(p1[0], p2[0])
        xmax = max(p1[0], p2[0])
        ymin = min(p1[1], p2[1])
        ymax = max(p1[1], p2[1])
        rect = box(xmin,ymin,xmax,ymax)
        rect_xy = [list(xy) for xy in list(zip(rect.exterior.coords.xy[0], rect.exterior.coords.xy[1]))]
        return self.format_geom([rect_xy], geom_type=self.geom_type)
    
    def poly_from_points(self, points):
        return self.format_geom([points], geom_type=self.geom_type)
    