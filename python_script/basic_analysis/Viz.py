import base64
from typing import List, Dict
import pandas as pd
import numpy as np


def color_graph() -> Dict[str, str]:
    dict_color_graph: Dict[str, str] = {'template': 'plotly_dark', 'plot_bgcolor': 'rgba(255, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'}
    return dict_color_graph


# def encode_image(list_image):
#     encoded: list() = []
#     img_encoded: list() = []
#     for image in list_image:
#         encoded.append(base64.b64encode(open(image, 'rb').read()))
#     for i in range(0, len(encoded)):
#         img_encoded.append('data:image/jpg;base64,{}'.format(encoded[i].decode()))
#     return img_encoded

