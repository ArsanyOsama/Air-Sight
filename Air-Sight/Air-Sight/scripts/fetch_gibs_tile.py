"""
fetch_gibs.py
Smart GIBS tile fetcher with stitching:
- Reads WMTSCapabilities
- Downloads multiple tiles
- Stitches into one map
"""

import requests, os
import xml.etree.ElementTree as ET
from datetime import datetime
from PIL import Image
from io import BytesIO

BASE_URL = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best"
CAPABILITIES = f"{BASE_URL}/1.0.0/WMTSCapabilities.xml"

OUT_DIR = "data/gibs"
os.makedirs(OUT_DIR, exist_ok=True)

def list_layers():
    resp = requests.get(CAPABILITIES)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"wmts": "http://www.opengis.net/wmts/1.0"}
    layers = {}
    for layer in root.findall(".//wmts:Layer", ns):
        identifier = layer.find("wmts:Identifier", ns).text
        title = layer.find("wmts:Title", ns).text
        tms = [link.attrib["tileMatrixSet"] for link in layer.findall(".//wmts:TileMatrixSetLink", ns)]
        layers[identifier] = {"title": title, "tileMatrixSets": tms}
    return layers

def fetch_tile(layer, date, matrixset, zoom, row, col):
    url = f"{BASE_URL}/{layer}/default/{date}/{matrixset}/{zoom}/{row}/{col}.png"
    resp = requests.get(url)
    if resp.status_code == 200 and resp.headers.get("Content-Type","").startswith("image"):
        return Image.open(BytesIO(resp.content))
    return None

def stitch_tiles(layer, date, matrixset="2km", zoom=3, rows=(2,4), cols=(4,6)):
    """Fetch and stitch multiple tiles into one image"""
    tiles = []
    for r in range(rows[0], rows[1]+1):
        row_tiles = []
        for c in range(cols[0], cols[1]+1):
            img = fetch_tile(layer, date, matrixset, zoom, r, c)
            if img:
                row_tiles.append(img)
        if row_tiles:
            tiles.append(row_tiles)

    if not tiles:
        print("❌ No tiles stitched")
        return

    # Stitch horizontally then vertically
    row_imgs = [Image.fromarray(
        sum([list(t.getdata()) for t in row], [])
    ) for row in tiles]

    widths, heights = zip(*(img.size for row in tiles for img in row))
    tile_w, tile_h = row_tiles[0].size
    total_w = tile_w * (cols[1]-cols[0]+1)
    total_h = tile_h * (rows[1]-rows[0]+1)

    stitched = Image.new("RGB", (total_w, total_h))
    y_offset = 0
    for r, row in enumerate(tiles):
        x_offset = 0
        for img in row:
            stitched.paste(img, (x_offset, y_offset))
            x_offset += img.size[0]
        y_offset += img.size[1]

    fname = os.path.join(OUT_DIR, f"{layer}_{date}_stitched.png")
    stitched.save(fname)
    print(f"✅ Stitched map saved → {fname}")

if __name__ == "__main__":
    today = datetime.utcnow().strftime("%Y-%m-%d")
    layers = list_layers()
    print("Available Layers (first 10):")
    for i,(id,info) in enumerate(list(layers.items())[:10]):
        print(f"{i+1}. {id} → {info['tileMatrixSets']}")

    # Example: NO2 tropospheric
    layer = "OMI_Nitrogen_Dioxide_Tropospheric_Column_Daily"
    stitch_tiles(layer, today, matrixset="2km", zoom=3, rows=(2,4), cols=(4,6))
