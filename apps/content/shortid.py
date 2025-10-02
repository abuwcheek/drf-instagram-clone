from hashids import Hashids

# Hashids sozlamasi
hashids = Hashids(
     min_length=8,  # Kod uzunligi kamida 8 ta belgi
     alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
)

def generate_shortcode(post_id: int) -> str:
     """Post ID dan short code yasash"""
     return hashids.encode(post_id)

def decode_shortcode(shortcode: str) -> int | None:
     """Short code ni qayta ID ga aylantirish"""
     decoded = hashids.decode(shortcode)
     return decoded[0] if decoded else None