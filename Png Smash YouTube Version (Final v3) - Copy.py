import png
import random
import re
import os

# Extract metadata from PNGs
def get_png_metadata(filepath):
    with open(filepath, 'rb') as f:
        pngdata = png.Reader(file=f)
        metadata = {}
        for chunk_type, chunk_data in pngdata.chunks():
            if chunk_type == b'tEXt':
                metadata[chunk_type] = chunk_data 
        #print(metadata)  
        return metadata

# Filter metadata and only get the tags
def extract_metadata_string(metadata):
    metadata_str = metadata[b'tEXt'].decode("utf-8")
    start = metadata_str.index("parameters\x00") + len("parameters\x00")
    end = metadata_str.index("\nNegative prompt:")
    return metadata_str[start:end]

folder_path = 'C:\PNG Smasher'  
png_files = os.listdir(folder_path)   

# We assume there are at least two PNG files in the folder
png_metadata = []
for png_file in png_files:
    filepath = os.path.join(folder_path, png_file)
    metadata = get_png_metadata(filepath)
    png_metadata.append(extract_metadata_string(metadata).split(','))

# Mashup time
tag_extraction_ratio = 1 # change this variable to control the number of tags extracted
extracted_tags = []

for metadata_list in png_metadata:
    num_tags_per_image = int(len(metadata_list) * tag_extraction_ratio)
    extracted_tags.extend(random.sample(metadata_list, num_tags_per_image))

output = ','.join(extracted_tags)
print(output)