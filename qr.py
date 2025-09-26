import qrcode

# Your number
number = 2546640350

# Convert to string (QR codes store text)
data = str(number)

# Create QR code
qr = qrcode.make(data)

# Save the image
qr.save("number_qr2.png")

# Optionally show it
qr.show()
