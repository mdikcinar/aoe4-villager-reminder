#!/usr/bin/env python3
"""
AoE4World API Test Script
Profile ID: 12345678
"""

import requests
import json
from datetime import datetime

def test_aoe4_api(profile_id: str = "12345678"):
    """Test AoE4World API for a given profile ID."""
    
    url = f"https://aoe4world.com/api/v0/players/{profile_id}/games/last"
    
    print("=" * 60)
    print(f"AoE4World API Test - Profile ID: {profile_id}")
    print("=" * 60)
    print(f"\n[ISTEK] URL: {url}\n")
    
    try:
        print("[INFO] API istegi gonderiliyor...")
        response = requests.get(url, timeout=10)
        
        print(f"\n[STATUS] Status Code: {response.status_code}")
        print(f"[HEADERS] Response Headers:")
        for key, value in response.headers.items():
            if key.lower() in ['content-type', 'content-length']:
                print(f"   {key}: {value}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n" + "=" * 60)
            print("[SUCCESS] BASARILI YANIT")
            print("=" * 60)
            
            # Önemli alanlar
            print("\n[MAC BILGILERI]")
            print(f"   Ongoing (Devam eden mac): {data.get('ongoing', False)}")
            
            if data.get('ongoing'):
                print("   [WARNING] SU ANDA DEVAM EDEN BIR MAC VAR!")
            else:
                print("   [INFO] Su anda devam eden mac yok")
            
            # Tarih bilgileri
            if 'started_at' in data and data['started_at']:
                started = data['started_at']
                print(f"\n[TARIH] Baslangic Zamani: {started}")
            
            if 'finished_at' in data and data['finished_at']:
                finished = data['finished_at']
                print(f"[TARIH] Bitis Zamani: {finished}")
            
            # Harita bilgisi
            if 'map' in data and data['map']:
                map_info = data['map']
                if isinstance(map_info, dict):
                    print(f"[HARITA] {map_info.get('name', 'N/A')}")
                else:
                    print(f"[HARITA] {map_info}")
            
            # Mod bilgisi
            if 'mode' in data and data['mode']:
                mode_info = data['mode']
                if isinstance(mode_info, dict):
                    print(f"[MOD] {mode_info.get('name', 'N/A')}")
                else:
                    print(f"[MOD] {mode_info}")
            
            # Sıralama bilgisi
            if 'ranked' in data:
                print(f"[RANKED] {data['ranked']}")
            
            # Süre bilgisi
            if 'duration' in data:
                duration = data['duration']
                if duration:
                    minutes = duration // 60
                    seconds = duration % 60
                    print(f"[SURE] {minutes} dakika {seconds} saniye")
            
            # Kazanan bilgisi
            if 'result' in data:
                result = data['result']
                if result == 'win':
                    print("[SONUC] KAZANDIN!")
                elif result == 'loss':
                    print("[SONUC] KAYBETTIN")
                elif result == 'draw':
                    print("[SONUC] BERABERE")
                else:
                    print(f"[SONUC] {result}")
            
            # Oynanan medeniyet
            if 'civilization' in data and data['civilization']:
                civ_info = data['civilization']
                if isinstance(civ_info, dict):
                    print(f"[MEDENIYET] {civ_info.get('name', 'N/A')}")
                else:
                    print(f"[MEDENIYET] {civ_info}")
            
            print("\n" + "=" * 60)
            print("[JSON] TAM JSON YANITI:")
            print("=" * 60)
            # Windows konsolu için ASCII-safe JSON
            json_str = json.dumps(data, indent=2, ensure_ascii=True)
            print(json_str)
            
        elif response.status_code == 404:
            print("\n" + "=" * 60)
            print("[ERROR] HATA: Profile ID bulunamadi")
            print("=" * 60)
            print(f"\n[WARNING] Status Code: {response.status_code}")
            print("[TIP] Profile ID'nin dogru oldugundan emin olun")
            print(f"   URL: {url}")
            
        else:
            print("\n" + "=" * 60)
            print(f"[WARNING] BEKLENMEYEN YANIT: {response.status_code}")
            print("=" * 60)
            print(f"\n[RESPONSE] Response Body:")
            print(response.text[:500])  # İlk 500 karakter
            
    except requests.Timeout:
        print("\n" + "=" * 60)
        print("[TIMEOUT] ZAMAN ASIMI")
        print("=" * 60)
        print("\n[ERROR] API istegi 10 saniye icinde yanit vermedi")
        
    except requests.ConnectionError:
        print("\n" + "=" * 60)
        print("[CONNECTION] BAGLANTI HATASI")
        print("=" * 60)
        print("\n[ERROR] Internet baglantinizi kontrol edin")
        
    except requests.RequestException as e:
        print("\n" + "=" * 60)
        print("[ERROR] ISTEK HATASI")
        print("=" * 60)
        print(f"\nHata: {str(e)}")
        
    except json.JSONDecodeError as e:
        print("\n" + "=" * 60)
        print("[ERROR] JSON PARSE HATASI")
        print("=" * 60)
        print(f"\nHata: {str(e)}")
        print(f"\nResponse Text: {response.text[:500]}")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("[ERROR] BEKLENMEYEN HATA")
        print("=" * 60)
        print(f"\nHata: {type(e).__name__}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Test tamamlandi")
    print("=" * 60)


if __name__ == "__main__":
    # Varsayılan olarak 12345678 kullan, ama komut satırından da değiştirilebilir
    import sys
    profile_id = sys.argv[1] if len(sys.argv) > 1 else "12345678"
    test_aoe4_api(profile_id)

