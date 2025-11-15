import random
import os
import json

KELIMELER = {
    "MEYVELER": ["ANANAS", "ŞEFTALİ", "MUZ", "ÇİLEK", "KİRAZ", "MANGO", "AVODAKO", "KARPUZ", "VİŞNE"],
    "HAYVANLAR": ["KEDİ", "KÖPEK", "KÖPEKBALIĞI", "YILAN", "TİLKİ", "ASLAN", "TİMSAH", "BALİNA"],
    "TEKNOLOJİ": ["BİLGİSAYAR", "TELEFON", "YAZILIM", "DONANIM", "İNTERNET", "YAPAYZEKA", "KOD"]
}
MAKS_HATA = 6
ILK_BONUS_PUANI = 15

ADAM_ASMACASI = [
    r"""
 +---+
 |  |
    |
    |
    |
    |
=========
""",
    r"""
 +---+
 |  |
 O  |
    |
    |
    |
=========
""",
    r"""
 +---+
 |  |
 O  |
 |  |
    |
    |
=========
""",
    r"""
 +---+
 |  |
 O  |
/|  |
    |
    |
=========
""",
    r"""
 +---+
 |  |
 O  |
/|\ |
    |
    |
=========
""",
    r"""
 +---+
 |  |
 O  |
/|\ |
/  |
    |
=========
""",
    r"""
 +---+
 |  |
 O  |
/|\ |
/ \ |
    |
=========
"""
]

PUANLAMA = {
    "doğru_harf": 10,
    "yanlış_harf": -5,
    "doğru_işlem": 15,
    "ipucu_kullanma": -1,
    "oyunu_kazanma": 50,
    "oyunu_kaybetme": -20
}
SKOR_DOSYASI = "scores.json"

def tr_to_en(text):
    return text.upper().replace('İ', 'I').replace('Ş', 'S').replace('Ğ', 'G').replace('Ü', 'U').replace('Ö',
                                                                                                        'O').replace(
        'Ç', 'C')

def rastgele_kelime_sec(kelimeler_sozluk):
    """Rastgele bir kelime seçer."""
    kategoriler = list(kelimeler_sozluk.keys())
    secilen_kategori = random.choice(kategoriler)
    kelime = random.choice(kelimeler_sozluk[secilen_kategori])
    return tr_to_en(kelime), tr_to_en(secilen_kategori)

def adam_asmaca_ciz(kalan_hata):
    yapilan_hata = MAKS_HATA - kalan_hata
    if 0 <= yapilan_hata <= MAKS_HATA:
        print(ADAM_ASMACASI[yapilan_hata])
    else:
        print(ADAM_ASMACASI[0])

def oyunu_goster(gizli_kelime, tahmin_edilen_harfler, kalan_hata, total_puan, bonus_puan, kategori):
    os.system('cls' if os.name == 'nt' else 'clear')

    print("--- ⚔️ HARF KURTARMA OPERASYONU ⚔️ ---")
    print(f"Kategori: **{kategori}**")
    print(f"Kalan Hata Hakkı: {kalan_hata}/{MAKS_HATA}")
    print(f"Toplam Puan: {total_puan} | Bonus Puanı (İpucu Hakkı): {bonus_puan}")
    print("---------------------------------------")

    adam_asmaca_ciz(kalan_hata)

    goruntulenen_kelime = ""
    kelime_tamamlandi = True
    for harf in gizli_kelime:
        if harf in tahmin_edilen_harfler:
            goruntulenen_kelime += harf + " "
        else:
            goruntulenen_kelime += "_ "
            kelime_tamamlandi = False

    print("\nGizli Kelime: ", goruntulenen_kelime)
    return kelime_tamamlandi

def hesap_cozme(gizli_kelime, tahmin_edilen_harfler, bonus_puan):
    sayi1 = random.randint(1, 10)
    sayi2 = random.randint(1, 10)
    islemler = ['+', '-', '*', '/']
    islem = random.choice(islemler)

    if islem == '/':
        sayi1 = sayi2 * random.randint(1, 10)
        if sayi1 == 0: sayi1 = sayi2

    try:
        if islem == '+':
            sonuc = sayi1 + sayi2
        elif islem == '-':
            sonuc = sayi1 - sayi2
        elif islem == '*':
            sonuc = sayi1 * sayi2
        elif islem == '/':
            sonuc = sayi1 // sayi2
    except ZeroDivisionError:
        return 0, bonus_puan, True

    print(f"\n### İşlem Çözme (Harf Açtırma Şansı) ###")
    print(f"İşlem: {sayi1} {islem} {sayi2} = ?")

    try:
        giris = input("Tahmininiz ('iptal' yazarak atlayabilirsiniz): ").upper()
        if giris == "İPTAL":
            print("İşlem atlandı.")
            return 0, bonus_puan, False

        tahmin = int(giris)

        if tahmin == sonuc:
            bilinmeyen_harfler = [h for h in gizli_kelime if h not in tahmin_edilen_harfler]

            if bilinmeyen_harfler:
                acilan_harf = random.choice(bilinmeyen_harfler)
                tahmin_edilen_harfler.add(acilan_harf)
                print(f"✅ Doğru! +{PUANLAMA['doğru_işlem']} Puan kazandınız. **'{acilan_harf}'** harfi açıldı.")
                return PUANLAMA['doğru_işlem'], bonus_puan, False
            else:
                print(f"✅ Doğru! +{PUANLAMA['doğru_işlem']} Puan kazandınız. (Tüm harfler zaten açık.)")
                return PUANLAMA['doğru_işlem'], bonus_puan, False
        else:
            print(f"❌ Yanlış. Doğru sonuç: {sonuc}. Hata hakkınız 1 azaldı.")
            return 0, bonus_puan, True

    except ValueError:
        print("❌ Geçersiz giriş. Hata hakkınız 1 azaldı.")
        return 0, bonus_puan, True

def ipucu_alma(kategori, bonus_puan):
    if bonus_puan >= 1:
        print(f"\n💡 İpucu: 1 bonus puanı harcandı. Kelimenin kategorisi: **{kategori}**")
        return PUANLAMA['ipucu_kullanma'], bonus_puan - 1
    else:
        print("\n❌ Yeterli bonus puanınız yok (En az 1 bonus puanı gereklidir).")
        return 0, bonus_puan

def skoru_kaydet(kullanici_adi, skor, kelime):
    "SKORLARI JSON DOSYASINA KAYDEDER"
    tum_skorlar = []
    try:
        if os.path.exists(SKOR_DOSYASI) and os.path.getsize(SKOR_DOSYASI) > 0:
            with open(SKOR_DOSYASI, "r", encoding="utf-8") as f:
                tum_skorlar = json.load(f)
    except Exception:
        pass

    tum_skorlar.append({
        "kullanici": kullanici_adi,
        "skor": skor,
        "kelime": kelime
    })

    tum_skorlar.sort(key=lambda x: x['skor'], reverse=True)

    try:
        with open(SKOR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(tum_skorlar, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Hata: Skorlar JSON dosyasına kaydedilemedi: {e}")

    print("\n### 🏆 En Yüksek 5 Skor ###")
    for i, s in enumerate(tum_skorlar[:5]):
        print(f"**{i + 1}.** {s['kullanici']} - **Puan:** {s['skor']} (Kelime: {s['kelime']})")

def oyunu_baslat():
    kullanici_adi = input("Lütfen adınızı girin: ")
    gizli_kelime, kategori = rastgele_kelime_sec(KELIMELER)

    tahmin_edilen_harfler = set()
    kalan_hata = MAKS_HATA
    total_puan = 0
    bonus_puan = ILK_BONUS_PUANI

    while kalan_hata > 0:

        kelime_tamamlandi = oyunu_goster(
            gizli_kelime, tahmin_edilen_harfler, kalan_hata, total_puan, bonus_puan, kategori
        )

        if kelime_tamamlandi:
            break

        print("\nSeçenekler: (H)arf Tahmin / (I)pucu Al / (C)özüm Yap")
        girdi = input("Seçiminiz: ").upper().replace('İ', 'I')

        if girdi == 'C':  # Harf Açtırma
            puan_degisimi, yeni_bonus, hata_alindi = hesap_cozme(gizli_kelime, tahmin_edilen_harfler, bonus_puan)
            total_puan += puan_degisimi
            bonus_puan = yeni_bonus
            if hata_alindi:
                kalan_hata -= 1
                print(f"⚠️ Hata hakkınız 1 azaldı. Kalan: {kalan_hata}")
            continue

        elif girdi == 'I':
            puan_degisimi, yeni_bonus = ipucu_alma(kategori, bonus_puan)
            total_puan += puan_degisimi
            bonus_puan = yeni_bonus
            continue

        elif girdi == 'H':
            tahmin = tr_to_en(input("Harf (tek) veya Tam Kelime Tahmininiz: "))

            if not tahmin:
                print("⚠️ Geçersiz giriş.")
                continue

            if len(tahmin) == 1: #Tek Harf Tahmini
                if not tahmin.isalpha():
                    print("⚠️ Lütfen geçerli bir harf girin.")
                    continue

                if tahmin in tahmin_edilen_harfler:
                    print(f"⚠️ Bu harfi ('{tahmin}') daha önce denediniz.")
                    continue

                tahmin_edilen_harfler.add(tahmin)

                if tahmin in gizli_kelime:
                    total_puan += PUANLAMA['doğru_harf']
                    bonus_puan += 1
                    print(f"✅ Doğru tahmin! +{PUANLAMA['doğru_harf']} Puan, +1 Bonus.")
                else:
                    total_puan += PUANLAMA['yanlış_harf']
                    kalan_hata -= 1
                    print(f"❌ Yanlış tahmin! {PUANLAMA['yanlış_harf']} Puan, -1 Hata. Kalan: {kalan_hata}")

            elif len(tahmin) > 1:
                if tahmin == gizli_kelime:
                    break
                else:
                    kalan_hata -= 1
                    print(f"❌ Yanlış tam kelime tahmini! Hata hakkınız 1 azaldı. Kalan: {kalan_hata}")

        else:
            print("⚠️ Geçersiz komut. Lütfen H, I veya C seçiniz.")

    print("\n=======================================")

    if kalan_hata <= 0:
        oyunu_goster(gizli_kelime, tahmin_edilen_harfler, kalan_hata, total_puan, bonus_puan, kategori)
        total_puan += PUANLAMA['oyunu_kaybetme']
        print(f"💀 KAYBETTİNİZ! Kelime: **{gizli_kelime}**. Final cezası: {PUANLAMA['oyunu_kaybetme']} puan.")
    else:
        total_puan += PUANLAMA['oyunu_kazanma']
        print(
            f"🎉 TEBRİKLER! Kelimeyi doğru tahmin ettiniz: **{gizli_kelime}**. Final bonusu: +{PUANLAMA['oyunu_kazanma']} puan.")

    print(f"OYUN SONU - Nihai Puanınız: {total_puan}")
    skoru_kaydet(kullanici_adi, total_puan, gizli_kelime)
    print("=======================================")

# Kodu çalıştırır
if __name__ == "__main__":
    oyunu_baslat()