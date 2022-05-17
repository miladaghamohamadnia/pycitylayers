# Geometry

> Auto-generated documentation for [pycitylayers.utils.geometry](../../../pycitylayers/utils/geometry.py) module.

- [Pycitylayers](../../README.md#pycitylayers) / [Modules](../../MODULES.md#pycitylayers-modules) / [Pycitylayers](../index.md#pycitylayers) / [Utils](index.md#utils) / Geometry
    - [GeometryGQL](#geometrygql)
        - [GeometryGQL().format_geom](#geometrygqlformat_geom)
    - [PointGQL](#pointgql)
        - [PointGQL().point](#pointgqlpoint)
    - [PolygonGQL](#polygongql)
        - [PolygonGQL().poly_from_points](#polygongqlpoly_from_points)
        - [PolygonGQL().rect_from_two_corners](#polygongqlrect_from_two_corners)

## GeometryGQL

[[find in source code]](../../../pycitylayers/utils/geometry.py#L4)

```python
class GeometryGQL():
    def __init__():
```

### GeometryGQL().format_geom

[[find in source code]](../../../pycitylayers/utils/geometry.py#L8)

```python
def format_geom(coords, epsg=4326, geom_type='Polygon'):
```

## PointGQL

[[find in source code]](../../../pycitylayers/utils/geometry.py#L19)

```python
class PointGQL(GeometryGQL):
    def __init__():
```

#### See also

- [GeometryGQL](#geometrygql)

### PointGQL().point

[[find in source code]](../../../pycitylayers/utils/geometry.py#L24)

```python
def point(x, y):
```

## PolygonGQL

[[find in source code]](../../../pycitylayers/utils/geometry.py#L31)

```python
class PolygonGQL(GeometryGQL):
    def __init__():
```

#### See also

- [GeometryGQL](#geometrygql)

### PolygonGQL().poly_from_points

[[find in source code]](../../../pycitylayers/utils/geometry.py#L45)

```python
def poly_from_points(points):
```

### PolygonGQL().rect_from_two_corners

[[find in source code]](../../../pycitylayers/utils/geometry.py#L36)

```python
def rect_from_two_corners(p1, p2):
```
