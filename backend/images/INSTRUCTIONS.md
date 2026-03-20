# How to Add Local Product Images

## Naming Convention
Place your product images in this folder with the following naming convention:
- `product_1.jpg` - Onion
- `product_2.jpg` - Potato  
- `product_3.jpg` - Tomato
- `product_4.jpg` - Apple
- `product_5.jpg` - Banana
- `product_6.jpg` - Mango
- `product_7.jpg` - Basmati Rice
- `product_8.jpg` - Wheat Atta
- `product_9.jpg` - Rava
- `product_10.jpg` - Toor Dal
- `product_11.jpg` - Moong Dal
- `product_12.jpg` - Chana Dal
- `product_13.jpg` - Turmeric Powder
- `product_14.jpg` - Red Chilli Powder
- `product_15.jpg` - Garam Masala
- `product_16.jpg` - Mustard Oil
- `product_17.jpg` - Sunflower Oil
- `product_18.jpg` - Pure Ghee
- `product_19.jpg` - Milk
- `product_20.jpg` - Curd
- `product_21.jpg` - Paneer

## Image Requirements
- **Format**: JPG or PNG
- **Size**: Recommended 400x400 pixels (will be resized to fit)
- **Quality**: Clear, high-quality product photos
- **Content**: Actual product images (onions, tomatoes, apples, etc.)

## How It Works
1. Place your image file in this folder with the correct name
2. Restart the backend server
3. The system will automatically use your local image
4. If no local image exists, it will fallback to online images

## Example
To add a custom onion image:
1. Save your onion photo as `product_1.jpg` in this folder
2. Restart the backend: `python simple_app.py`
3. Your custom onion image will now appear on the website
