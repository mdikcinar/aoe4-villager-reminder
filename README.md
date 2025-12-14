# AoE4 Villager Reminder

Age of Empires 4 için villager üretim hatırlatıcı uygulaması. Oyun sırasında belirli aralıklarla köylü üretmenizi hatırlatır.

![Screenshot](docs/screenshot.png)

## Özellikler

- **Otomatik Oyun Algılama**: Oyun başladığında otomatik olarak timer'ı başlatır
  - Process algılama (önerilen)
  - AoE4World API entegrasyonu
  - Manuel mod
- **Ses ve Popup Bildirimleri**: Her uyarıda ses çalar ve popup gösterir
- **İstatistik Takibi**: Oyun süresi, uyarı sayısı gibi istatistikleri kaydeder
- **Ayarlanabilir Timer**: 5-60 saniye arası timer süresi
- **System Tray**: Arka planda çalışır, tray'den kontrol edilebilir
- **Modern Arayüz**: AoE4 temasına uygun dark theme

## Kurulum

### Hazır Exe (Önerilen)

1. [Releases](https://github.com/yourusername/aoe4-villager-reminder/releases) sayfasından son sürümü indirin
2. `AoE4VillagerReminder.exe` dosyasını çalıştırın

### Kaynak Koddan Çalıştırma

1. Python 3.11+ yükleyin
2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```bash
   python main.py
   ```

## Kullanım

### Oyun Algılama Yöntemleri

1. **Process (Önerilen)**: AoE4'ün çalışıp çalışmadığını kontrol eder. En güvenilir yöntemdir.
2. **API**: AoE4World API'den aktif oyun kontrolü yapar. Profile ID gerektirir.
3. **Manuel**: Timer'ı kendiniz başlatıp durdurursunuz.

### Ayarlar

- **Uyarı Aralığı**: Köylü üretim süresi (varsayılan 25 saniye)
- **Ses Seviyesi**: Uyarı sesinin yüksekliği
- **Popup Bildirimi**: Windows bildirim gösterimi
- **Her Zaman Üstte**: Pencereyi diğer pencerelerin üstünde tutar

### System Tray

Pencereyi kapatınca uygulama system tray'e küçülür. Tray ikonuna:
- Çift tıklayarak pencereyi açabilirsiniz
- Sağ tıklayarak menüye erişebilirsiniz

## Exe Oluşturma

```bash
pyinstaller --name="AoE4VillagerReminder" --windowed --onefile --add-data="assets;assets" main.py
```

## Lisans

MIT License

## Katkıda Bulunma

Pull request'ler kabul edilir. Büyük değişiklikler için önce bir issue açın.

## İletişim

Sorular ve öneriler için issue açabilirsiniz.


