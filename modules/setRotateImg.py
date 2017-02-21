# -*- encoding:utf-8 -*-

from PIL import Image,JpegImagePlugin
from cStringIO import StringIO
import io

def img_reset(byte):
  convert_image = {
    1: lambda img: img,
    2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    3: lambda img: img.transpose(Image.ROTATE_180),
    4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90),
    6: lambda img: img.transpose(Image.ROTATE_270),
    7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270),
    8: lambda img: img.transpose(Image.ROTATE_90),
  }
  img = Image.open(StringIO(byte))
  img.thumbnail((1600, 1600), Image.ANTIALIAS)
  new_img = img

  if img.format == "JPEG":
    exif = img._getexif()
    if exif:
      orientation = exif.get(0x112, 1)
      new_img = convert_image[orientation](img)

  return new_img 

def landmarks_to_clm(marks):
  marks = marks.tolist()
  clm = [None for row in range(71)]
  clm[0] = marks[0]
  clm[1] = marks[1]
  clm[2] = marks[2]
  clm[3] = marks[3]
  clm[4] = marks[5]
  clm[5] = marks[6]
  clm[6] = marks[7]
  clm[7] = marks[8]
  clm[8] = marks[9]
  clm[9] = marks[10]

  clm[10] = marks[11]
  clm[11] = marks[13]
  clm[12] = marks[14]
  clm[13] = marks[15]
  clm[14] = marks[16]
  clm[15] = marks[26]
  clm[16] = marks[25]
  clm[17] = marks[23]
  clm[18] = marks[22]
  clm[19] = marks[17]


  clm[20] = marks[18]
  clm[21] = marks[20]
  clm[22] = marks[21]
  clm[23] = marks[36]
  point = (marks[38][0] - marks[37][0])/2
  clm[24] = [marks[37][0]+point,marks[37][1]]
  clm[25] = marks[39]
  point = (marks[40][0] - marks[41][0])/2
  clm[26] = [marks[41][0] + point,marks[41][1]]
  clm[27] = [marks[41][0]+point,marks[39][1]]
  clm[28] = marks[45]
  point = (marks[44][0]-marks[43][0])/2
  clm[29] = [marks[43][0]+point,marks[43][1]]

  clm[30] = marks[42]
  point = (marks[46][0] - marks[47][0])/2
  clm[31] = [marks[47][0]+point,marks[47][1]]
  clm[32] = [marks[47][0]+point,marks[42][1]]
  clm[33] = marks[27]
  clm[34] = marks[31] #++++++++++++
  clm[35] = marks[31] #++++++++++++
  clm[36] = marks[31]
  clm[37] = marks[33]
  clm[38] = marks[35]
  clm[39] = marks[35] #++++++++++++

  clm[40] = marks[35] #++++++++++++
  clm[41] = marks[29] #++++++++++++
  clm[42] = marks[32]
  clm[43] = marks[34]
  clm[44] = marks[48]
  clm[45] = marks[49]
  clm[46] = marks[50]
  clm[47] = marks[51]
  clm[48] = marks[52]
  clm[49] = marks[53]

  clm[50] = marks[54]
  clm[51] = marks[55]
  clm[52] = marks[56]
  clm[53] = marks[57]
  clm[54] = marks[58]
  clm[55] = marks[59]
  clm[56] = marks[67]
  clm[57] = marks[66]
  clm[58] = marks[65]
  clm[59] = marks[63]

  clm[60] = marks[62]
  clm[61] = marks[61]
  clm[62] = marks[30]
  clm[63] = marks[37]
  clm[64] = marks[38]
  clm[65] = marks[40]
  clm[66] = marks[41]
  clm[67] = marks[44]
  clm[68] = marks[43]
  clm[69] = marks[47]

  clm[70] = marks[46]
  return clm
