import os
from PIL import Image
Image.init()

output_dir = 'Certificates'
pdf_path = 'All_Certificates.pdf'

image_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.png')]
image_files.sort()

if not image_files:
    print("No certificates found!")
    exit()

print(f"Compiling {len(image_files)} certificates into a single PDF...")

first_image = Image.open(image_files[0]).convert('RGB')
image_list = []
for file in image_files[1:]:
    img = Image.open(file).convert('RGB')
    image_list.append(img)

first_image.save(pdf_path, save_all=True, append_images=image_list)
print(f"Successfully created {pdf_path} with {len(image_files)} pages.")
