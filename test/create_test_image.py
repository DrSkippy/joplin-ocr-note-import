#!/usr/bin/env python3
"""Create a test image with text for OCR testing."""
from PIL import Image, ImageDraw, ImageFont

# Create a white image
img = Image.new('RGB', (800, 400), color='white')
draw = ImageDraw.Draw(img)

# Add text
text = """Invoice #12345
Date: 2026-01-13

Item: Coffee Beans
Quantity: 2
Price: $25.99

Total: $51.98

Thank you for your business!"""

# Try to use a default font, fall back to basic if not available
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except:
    font = ImageFont.load_default()

# Draw text on image
draw.text((50, 50), text, fill='black', font=font)

# Save the image
img.save('test/sample_invoice.png')
print("Test image created: test/sample_invoice.png")
