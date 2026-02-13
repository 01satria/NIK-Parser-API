from flask import Flask, jsonify, request
import json
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# URL data wilayah (dari sumber terpercaya)
URL_PROV = "https://raw.githubusercontent.com/yusufsyaifudin/wilayah-indonesia/master/data/list_of_area/provinces.json"
URL_KAB = "https://raw.githubusercontent.com/yusufsyaifudin/wilayah-indonesia/master/data/list_of_area/regencies.json"
URL_KEC = "https://raw.githubusercontent.com/yusufsyaifudin/wilayah-indonesia/master/data/list_of_area/districts.json"

# Cache data (load sekali saat app start)
PROVINSI = {p['id']: {'nama': p['name']} for p in requests.get(URL_PROV).json()}
KABUPATEN = {k['id']: {'nama': k['name'], 'kode_provinsi': k['province_id'],
                       'jenis': 'Kabupaten' if k['name'].startswith('KABUPATEN') else 'Kota'}
             for k in requests.get(URL_KAB).json()}
KECAMATAN = {str(k['id']): {'nama': k['name'], 'kode_kabupaten': k['regency_id']}
             for k in requests.get(URL_KEC).json()}

# Data pendukung
BULAN_ID = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
PASARAN_JAWA = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
HARI_JAWA = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
ZODIAK = [(120, "Capricorn"), (219, "Aquarius"), (321, "Pisces"), (420, "Aries"), (521, "Taurus"), (622, "Gemini"),
          (723, "Cancer"), (823, "Leo"), (923, "Virgo"), (1023, "Libra"), (1123, "Scorpio"), (1222, "Sagittarius"), (1232, "Capricorn")]

def get_zodiak(day, month):
    mmdd = month * 100 + day
    for limit, name in ZODIAK:
        if mmdd <= limit:
            return name
    return "Capricorn"

def hitung_pasaran(tgl: datetime):
    # Aproksimasi weton: ref 1 Jan 1900 = Senin Wage
    ref_date = datetime(1900, 1, 1)
    delta = (tgl - ref_date).days
    hari_idx = delta % 7  # 0=Minggu, 1=Senin, ...
    pasaran_idx = (delta + 1) % 5  # Sesuaikan agar match contoh (21 Aug 2006 = Senin Kliwon)
    return f"{HARI_JAWA[hari_idx]} {PASARAN_JAWA[pasaran_idx]}"

def hitung_usia(tgl_lahir: datetime, sekarang: datetime):
    delta = sekarang - tgl_lahir
    tahun = delta.days // 365
    sisa_hari = delta.days % 365
    bulan = sisa_hari // 30
    hari = sisa_hari % 30
    return f"{tahun} Tahun {bulan} Bulan {hari} Hari"

def kategori_usia(tahun: int):
    if tahun < 5: return "Balita"
    elif tahun < 12: return "Anak-anak"
    elif tahun < 18: return "Remaja"
    elif tahun < 40: return "Dewasa"
    elif tahun < 60: return "Paruh Baya"
    return "Lansia"

def ultah_berikutnya(tgl_lahir: datetime, sekarang: datetime):
    next_birthday = tgl_lahir.replace(year=sekarang.year)
    if next_birthday < sekarang:
        next_birthday = next_birthday.replace(year=sekarang.year + 1)
    delta = next_birthday - sekarang
    bulan = delta.days // 30
    hari = delta.days % 30
    return f"{bulan} Bulan {hari} Hari Lagi" if delta.days > 0 else "Hari Ini!"

def parse_nik(nik: str, sekarang: datetime = datetime.now()):
    if len(nik) != 16 or not nik.isdigit():
        return {"status": False, "message": "NIK invalid: Harus 16 digit angka."}

    prov = nik[:2]
    kab = nik[:4]
    kec = nik[:6]
    tgl = int(nik[6:8])
    bln = int(nik[8:10])
    thn = int(nik[10:12])
    urut = nik[12:16]

    # Jenis kelamin & tanggal
    kelamin = "PEREMPUAN" if tgl > 40 else "LAKI-LAKI"
    tgl = tgl - 40 if tgl > 40 else tgl
    tahun_lahir = 2000 + thn if thn < datetime.now().year % 100 else 1900 + thn

    try:
        tgl_lahir = datetime(tahun_lahir, bln, tgl)
    except ValueError:
        return {"status": False, "message": "Tanggal lahir invalid."}

    lahir = f"{tgl:02d}/{bln:02d}/{thn:02d}"
    lahir_lengkap = f"{tgl} {BULAN_ID[bln]} {tahun_lahir}"

    # Wilayah
    prov_data = PROVINSI.get(prov, {'nama': 'Tidak Diketahui'})
    kab_data = KABUPATEN.get(kab, {'nama': 'Tidak Diketahui', 'jenis': '??'})
    kec_data = KECAMATAN.get(kec, {'nama': 'Tidak Diketahui'})

    # Tambahan
    pasaran = hitung_pasaran(tgl_lahir)
    usia = hitung_usia(tgl_lahir, sekarang)
    tahun_usia = int(usia.split()[0])
    kat_usia = kategori_usia(tahun_usia)
    ultah = ultah_berikutnya(tgl_lahir, sekarang)
    zodiak = get_zodiak(tgl, bln)

    result = {
        "nik": nik,
        "kelamin": kelamin,
        "lahir": lahir,
        "lahir_lengkap": lahir_lengkap,
        "provinsi": {"kode": prov, "nama": prov_data['nama']},
        "kotakab": {"kode": kab, "nama": kab_data['nama'], "jenis": kab_data['jenis']},
        "kecamatan": {"kode": kec, "nama": kec_data['nama']},
        "kode_wilayah": f"{prov}.{kab[2:4]}.{kec[4:6]}",
        "nomor_urut": urut,
        "tambahan": {
            "pasaran": f"{pasaran}, {lahir_lengkap}",
            "usia": usia,
            "kategori_usia": kat_usia,
            "ultah": ultah,
            "zodiak": zodiak
        }
    }

    return {"creator": "SatriaDev", "status": True, "result": result}

@app.route('/parse_nik', methods=['GET'])
def api_parse_nik():
    nik = request.args.get('nik')
    if not nik:
        return jsonify({"status": False, "message": "Parameter 'nik' diperlukan."}), 400
    result = parse_nik(nik)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)