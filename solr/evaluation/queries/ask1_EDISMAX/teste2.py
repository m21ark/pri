from PIL import Image


def change_pixel_color(source_image_path, target_image_path, output_path, target_color, new_color):
    # Open the source image
    source_img = Image.open(source_image_path)

    # Open the target image
    target_img = Image.open(target_image_path)

    new_rgb = tuple(int(new_color[i:i + 2], 16) for i in (0, 2, 4))

    # Get the source image data
    source_data = source_img.getdata()

    new_data = []
    for pixel in source_data:
        if pixel[0] < pixel[2] and pixel[1] < pixel[2]:
            new_data.append(new_rgb)
        else:
            new_data.append((0, 0, 0, 0))  # Add a transparent pixel

    new_img = Image.new("RGBA", source_img.size)
    new_img.putdata(new_data)

    # Paste the modified source image onto the target image
    target_img.paste(new_img, (0, 0), new_img)

    # Save the new target image
    target_img.save(output_path)

if __name__ == "__main__":
    # Replace 'input_source.png' with the path to your source image
    source_image_path = "precision_recall_V1.png"

    # Replace 'input_target.png' with the path to your target image
    target_image_path = "precision_recall_V2.png"
    
    # Replace 'output.png' with the desired output path
    output_image_path = "output.png"

    # Replace '1F77B4' and 'FF0000' with the target and new colors, respectively
    target_color = "1F77B4"
    new_color = "FF0000"

    change_pixel_color(source_image_path, target_image_path, output_image_path, target_color, new_color)

    print(f"Conversion complete. Image saved to {output_image_path}")

