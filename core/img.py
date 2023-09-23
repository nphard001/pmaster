"""
Info hidden by stable diffusion UI
"""
import imageio
import piexif
import piexif.helper


def read_pstring(abspath: str):
    if abspath.endswith('png'):
        reader = imageio.get_reader(abspath)
        meta = reader.get_meta_data()
        return meta['parameters']
    else:
        return read_pstring_jpg(abspath)

def read_pstring_jpg(abspath: str):
    exif = piexif.load(abspath)
    exif_comment = (exif or {}).get("Exif", {}).get(piexif.ExifIFD.UserComment, b'')
    try:
        exif_comment = piexif.helper.UserComment.load(exif_comment)
    except ValueError:
        exif_comment = exif_comment.decode('utf8', errors="ignore")
    return exif_comment

def parse_pstring(raw: str):
    data = {'raw': raw}
    p1, p2 = raw.split("Negative prompt: ")
    data['pos'] = p1.replace('\n', '')
    p2, p3 = p2.split("Steps: ")
    data['neg'] = p2
    p3 = f"Steps: {p3}"
    data['model'] = p3
    return data
