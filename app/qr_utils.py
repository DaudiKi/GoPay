import os
import qrcode
from io import BytesIO

def generate_payment_qr(driver_id: str) -> bytes:
    """
    Generate QR code for driver payment URL.
    
    Args:
        driver_id: The unique identifier for the driver
        
    Returns:
        Bytes of the QR code image in PNG format
    """
    # Get base URL from environment
    base_url = os.getenv('BASE_PUBLIC_URL')
    
    # Generate payment URL
    payment_url = f"{base_url}/pay?driver_id={driver_id}"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(payment_url)
    qr.make(fit=True)
    
    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_buffer = BytesIO()
    qr_image.save(img_buffer, format='PNG')
    return img_buffer.getvalue()







