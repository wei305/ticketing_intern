import os
import re

import ddddocr
from PIL import Image


ocr = ddddocr.DdddOcr()


def main():
    root_dir = os.path.dirname(__file__)
    resources_dir = 'resources'
    files = []
    for path in os.listdir(resources_dir):
        files.append(path)

    for file in files:
        abs_file_path = os.path.join(root_dir, resources_dir, file)
        image = Image.open(abs_file_path)

        result = ocr.classification(image)

        expected = re.search(r'code-(.+)\.png', file).group(1)
        print(f'expected {expected}, got {result}')
        assert expected == result, f'expected {expected}, got {result}'



if __name__ == '__main__':
    main()
