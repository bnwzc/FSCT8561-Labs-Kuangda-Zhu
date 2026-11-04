import base64
import csv
from pathlib import Path
from PIL import Image, ExifTags
import re

image_dir = Path("Images")
results = []

def exif_metadata(image_path):
    with Image.open(image_path) as img:
        exif = img.getexif()
        for tag_id, value in exif.items():
            if type(value) == str:
                try:
                    decoded_value = base64.b64decode(value).decode("utf-8")
                except:
                    decoded_value = value
                if any(keyword in value.upper() for keyword in ["RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL"]):
                    return value
                elif any(keyword in decoded_value.upper() for keyword in ["RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL"]):
                    return [decoded_value, "base64"]
    return None


def png_metadata(image_path):
    with Image.open(image_path) as img:
        for key, value in img.info.items():
            if isinstance(value, str):
                if type(value) == str:
                    if any(keyword in value.upper() for keyword in ["RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL"]):
                        return value
    return None

def xmp_metadata(image_path):
    with Image.open(image_path) as img:
        xmp = img.info.get("XML:com.adobe.xmp") or img.info.get("xmp")
        if isinstance(xmp, bytes):
            xmp = xmp.decode("utf-8", errors="replace")
        if xmp:
            if any(keyword in xmp.upper() for keyword in ["RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL"]):
                text = re.search(r'<exif:MakerNote>(.*?)</exif:MakerNote>', xmp, re.DOTALL).group(1).strip()
                return text

def hide_metadata(image_path):
    with Image.open(image_path) as img:
        exif_bytes = img.info.get("exif", b"")
        exif_text = exif_bytes.decode("utf-8", errors="ignore")
                
        if any(keyword in exif_text.upper() for keyword in ["RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL"]):
            pattern = rf"\b({'|'.join(["RECON", "VULN", "EXPLOIT", "PERSIST", "LATERAL", "EXFIL"])}):.*?\."
            match = re.search(pattern, exif_text, re.IGNORECASE)
            
            if match:
                return match.group(0)
            
        return None

for image_path in sorted(image_dir.glob("*.png")):
    with Image.open(image_path) as img:
        suspected_field = ""
        encoding = "plain text"
        risk_score = 0
        reason = ""
        
        if exif_metadata(image_path):
            try:
                suspected_field, reason = "EXIF", "Found: " + exif_metadata(image_path)
                risk_score = 10
            except:
                suspected_field = "EXIF"
                reason, encoding = "Found: " + exif_metadata(image_path)[0], exif_metadata(image_path)[1]
        elif png_metadata(image_path):
            suspected_field, reason = "PNG", "Found: " + png_metadata(image_path)
            risk_score = 10
        elif xmp_metadata(image_path):
            suspected_field, reason = "XMP", "Found: " + xmp_metadata(image_path)
            risk_score = 10
        else:
            suspected_field, reason = "EXIF", "Found: " + hide_metadata(image_path)
            risk_score = 10

        
        result = {
            "filename": image_path.name,
            "format": img.format,
            "metadata_fields": ", ".join(img.info.keys()),
            "suspected_field": suspected_field,    # TODO: identify relevant EXIF, PNG, or XMP field
            "encoding": encoding,           # TODO: indicate Base64, plain text, etc.
            "risk_score": risk_score,          # TODO: apply and justify your scoring rules
            "reason": reason,             # TODO: explain evidence for this score
        }
        # TODO: inspect EXIF metadata
        # TODO: inspect PNG text metadata and XMP metadata
        # TODO: identify covert-message indicators and update result
        results.append(result)

with open("metadata_report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Saved", len(results), "rows to metadata_report.csv")