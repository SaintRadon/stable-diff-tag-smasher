import gradio as gr
import random
import png

def extract_metadata(filepath):
    try:
        with open(filepath, 'rb') as f:
            pngdata = png.Reader(file=f)
            metadata = {}
            for chunk_type, chunk_data in pngdata.chunks():
                if chunk_type == b'tEXt':
                    metadata[chunk_type] = chunk_data 
            start = metadata[b'tEXt'].decode("utf-8").index("parameters\x00") + len("parameters\x00")
            end = metadata[b'tEXt'].decode("utf-8").index("\nNegative prompt:")
            filter_metadata = metadata[b'tEXt'].decode("utf-8")[start:end].split(',')
        return filter_metadata
    except :
        return "no png data detected"


def get_png_metadata(filepath1, filepath2, tag_ratio1, tag_ratio2):
    filter_metadata1 = extract_metadata(filepath1)
    filter_metadata2 = extract_metadata(filepath2)
    
    if filter_metadata1 == "no png data detected" or filter_metadata2 == "no png data detected":
        return "no png data detected"
    
    tags_per_image1 = int(len(filter_metadata1) * tag_ratio1)
    tags_per_image2 = int(len(filter_metadata2) * tag_ratio2)
    
    extracted_tags1 = random.sample(filter_metadata1, tags_per_image1)
    extracted_tags2 = random.sample(filter_metadata2, tags_per_image2)
    
    combined_tags = (extracted_tags1 + extracted_tags2)
    output = ','.join(combined_tags) 
    
    return output


demo = gr.Interface(
    fn=get_png_metadata, 
    inputs=["text", "text", gr.Slider(0,1), gr.Slider(0,1)],
    outputs="text",
    )

demo.launch()