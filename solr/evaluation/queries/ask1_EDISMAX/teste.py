from PIL import Image

def change_pixel_color(image_path, target_color, new_color, output_path):
    # Open the image
    img = Image.open(image_path)

    new_rgb = tuple(int(new_color[i:i + 2], 16) for i in (0, 2, 4))

    # Get the image data
    data = img.getdata()


    new_data = []
    for pixel in data:
         if pixel[0] < pixel[2] and pixel[1] < pixel[2]:
            new_data.append(new_rgb)
         else:
            new_data.append(pixel)
         
        
    new_img = Image.new("RGB", img.size)
    new_img.putdata(new_data)

    # Save the new image
    new_img.save(output_path)

if __name__ == "__main__":
    # Replace 'input.png' with the path to your input image
    input_image_path = "precision_recall_V2.png"
    
    # Replace 'output.png' with the desired output path
    output_image_path = "precision_recall_V2.png"

    # Replace '13FFAA' and '123463' with the target and new colors, respectively
    target_color = "1F77B4"
    new_color = "0000FF"

    change_pixel_color(input_image_path, target_color, new_color, output_image_path)

    print(f"Conversion complete. Image saved to {output_image_path}")

