def format_waktu(detik):
    menit = detik // 60
    sisa_detik = detik % 60
    return f"{menit:02d}:{sisa_detik:02d}"

print(format_waktu(150))  # Output: 02:30