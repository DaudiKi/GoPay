import os
import qrcode
from io import BytesIO

def generate_payment_qr(driver_id: str, passenger_phone: str = None) -> bytes:
    """
    Generate QR code for driver payment URL.
    
    Args:
        driver_id: The unique identifier for the driver
        passenger_phone: Optional phone number to pre-fill in payment form
        
    Returns:
        Bytes of the QR code image in PNG format
    """
    # Get base URL from environment
    base_url = os.getenv('BASE_PUBLIC_URL')
    if not base_url:
        # Fallback to localhost if BASE_PUBLIC_URL not set
        base_url = "http://localhost:8000"
    
    # Remove any trailing slashes
    base_url = base_url.rstrip('/')
    
    # Generate payment URL
    payment_url = f"{base_url}/pay?driver_id={driver_id}"
    if passenger_phone:
        payment_url += f"&phone={passenger_phone}"
    
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







