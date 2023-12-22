import threading
import requests
import binascii
import hashlib
import random
import base64
import uuid
import time
import json
import os

from pystyle import Col
from utils.ttencrypt import TTEncrypt
from utils.xlog import XLEncrypt
from utils.gorgon import Gorgon
from utils.solver import PuzzleSolver
from urllib.parse import urlencode


APP = {
    "version_code"  : 160904,
    "sig_hash"      : "aea615ab910015038f73c47e45d21466",
    "version"       : "16.9.4",
    "release_build" : "f05822b_20201014",
    "git_hash"      : "9f888696",
    "aid"           : 1340
}

START = time.time()

class Utils:
    @staticmethod
    def _xor(string):
        encrypted = [hex(ord(c) ^ 5)[2:] for c in string]
        return "".join(encrypted)

    @staticmethod
    def _sig(params: str, body: str = None, cookie: str = None):
        gorgon = Gorgon()
        return gorgon.calculate(params, cookie, body)
    
    @staticmethod
    def _ttencrypt(body: dict) -> str:
        ttencrypt = TTEncrypt()
        data_formated = json.dumps(body).replace(" ", "")
        return ttencrypt.encrypt(data_formated)
    
    @staticmethod
    def _xlencrypt(body: str) -> str:
        return XLEncrypt().encrypt(body)
    
    @staticmethod
    def _fch(xlog: str):
        xlog = xlog[0:len(xlog) - 21]
        fch_str = binascii.crc32(xlog.encode("utf-8"))
        fch_str = str(fch_str)

        for i in range(len(fch_str), 10):
            fch_str = '0' + fch_str

        return fch_str
    
    @staticmethod
    def sprint(x: str, num: int, msg: str) -> None:
        return '    %s{%s%s%s}%s %s %s[%s%s%s]%s' % (
            Col.purple, Col.reset,
            x, 
            Col.purple, Col.reset,
            num,
            Col.blue, Col.reset,
            msg,
            Col.blue, Col.reset
        )

class Device:
    @staticmethod
    def __openudid() -> str:
        return binascii.hexlify(random.randbytes(8)).decode()
    
    @staticmethod
    def __uuid() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def __install_time() -> int:
        return int(round(time.time() * 1000)) - random.randint(13999, 15555)
    
    @staticmethod
    def __ut() -> str:

        return random.randint(100, 500)
    
    @staticmethod
    def __uid() -> int:
        return random.randrange(10000, 10550, 50)

    @staticmethod
    def __ts() -> int:
        return round(random.uniform(1.2, 1.6) * 100000000) * -1

    @staticmethod
    def __cba() -> str:
        return f"0x{random.randbytes(4).hex()}"
    
    @staticmethod
    def __hc() -> str:
        return f"0016777{random.randint(260, 500)}"
    
    @staticmethod
    def __dp() -> str:
        return f"{random.randint(700000000, 900000000)},0,0"
    
    @staticmethod
    def __rom() -> int:
        return str(random.randint(700000000, 799999999))
    
    @staticmethod
    def gen_device() -> dict:
        return {
            "device_model"  : "SM-G9550",
            "device_serial" : "G9550",
            "resolution"    : "1600x900",
            "resolution2"   : "900*1600",
            "device_brand"  : "samsung",
            "openudid"      : Device.__openudid(),
            "google_aid"    : Device.__uuid(),
            "clientudid"    : Device.__uuid(),
            "cdid"          : Device.__uuid(),
            "req_id"        : Device.__uuid(),
            "install_time"  : Device.__install_time(),
            "ut"            : Device.__ut(),
            "ts"            : Device.__ts(),
            "cba"           : Device.__cba(),
            "hc"            : Device.__hc(),
            "dp"            : Device.__dp(),
            "rom"           : Device.__rom(),
            "uid"           : Device.__uid(),
            "tz_name"       : "Africa\/Harare",
            "tz_offset"     : 7200,
            "device_id"     : 0000000000000000000,
            "install_id"    : 0000000000000000000,
            "install_time"  : int(round(time.time() * 1000)) - random.randint(13999, 15555)
        }

class Applog:
    def __init__(self, device: dict or None = None, proxy: str or None = None) -> tuple:
        self.__device = Device.gen_device() if device is None else device
        self.__host   = "log-va.tiktokv.com"
        self.proxies = {'http': f'http://{proxy}', 'http': f'http://{proxy}'} if proxy else None

    def __get_headers(self, params: str, payload: bytes):
        sig = Utils._sig(
            params = params, 
            body   = payload
        )
        
        return {
            "x-ss-stub"             : str(hashlib.md5(payload).hexdigest()).upper(),
            "accept-encoding"       : "gzip",
            "passport-sdk-version"  : "17",
            "sdk-version"           : "2",
            "x-ss-req-ticket"       : str(int(time.time()) * 1000),
            "x-gorgon"              : sig["X-Gorgon"],
            "x-khronos"             : sig["X-Khronos"],
            "content-type"          : "application/octet-stream;tt-data=a",
            "host"                  : "log-va.tiktokv.com",
            "connection"            : "Keep-Alive",
            "user-agent"            : "okhttp/3.10.0.1"
        }

    def __get_params(self):
        
        return urlencode(
            {
                "ac"                    : "wifi",
                "channel"               : "googleplay",
                "aid"                   : APP["aid"],
                "app_name"              : "musically_go",
                "version_code"          : APP["version_code"],
                "version_name"          : APP["version"],
                "device_platform"       : "android",
                "ab_version"            : APP["version"],
                "ssmix"                 : "a",
                "device_type"           : self.__device["device_model"],
                "device_brand"          : self.__device["device_brand"],
                "language"              : "en",
                "os_api"                : 25,
                "os_version"            : "7.1.2",
                "openudid"              : self.__device["openudid"],
                "manifest_version_code" : APP["version_code"],
                "resolution"            : self.__device["resolution"],
                "dpi"                   : 320,
                "update_version_code"   : APP["version_code"],
                "_rticket"              : [int(time.time() * 1000), int(time.time() * 1000) + 111],
                "storage_type"          : 0,
                "app_type"              : "normal",
                "sys_region"            : "US",
                "pass-route"            : 1,
                "pass-region"           : 1,
                "timezone_name"         : self.__device["tz_name"],
                "timezone_offset"       : self.__device["tz_offset"],
                "carrier_region_v2"     : 310,
                "cpu_support64"         : "false",
                "host_abi"              : "armeabi-v7a",
                "ts"                    : [int(time.time()), time.time() + 2],
                "build_number"          : APP["version"],
                "region"                : "US",
                "uoo"                   : 0,
                "app_language"          : "en",
                "carrier_region"        : "IE",
                "locale"                : "en",
                "op_region"             : "IE",
                "ac2"                   : "wifi",
                "cdid"                  : self.__device["cdid"],
                "tt_data"               : "a"
            }
        )
    
    def __get_payload(self):
        
        return {
            "magic_tag":"ss_app_log",
            "header": {
                # removed from preview
            },
            "_gen_time": int(round(time.time() * 1000))
        }
        
    def register_device(self):
        for x in range(5):
            try:
                params  = self.__get_params()
                payload = bytes.fromhex(Utils._ttencrypt(self.__get_payload()))

                r = requests.post(
                    url = (
                        "http://" + 
                            self.__host
                            + "/service/2/device_register/?" 
                            + params
                    ),
                    headers = self.__get_headers(params, payload),
                    data    = payload,
                    proxies = self.proxies
                )

                if len(str(r.json()["device_id"])) > 6:

                    self.__device["device_id"]  = r.json()["device_id"]
                    self.__device["install_id"] = r.json()["install_id"]

                    # print(
                    #     Utils.sprint(
                    #         "*", 0, "Applog Sucess %s%s%s | %s%s%s" % (
                    #             Col.blue,
                    #             self.__device["device_id"], 
                    #             Col.reset,
                    #             Col.blue,
                    #             self.__device["install_id"],
                    #             Col.reset
                    #         )
                    #     )
                    # )
                    
                    return self.__device
            except:
                continue

class Xlog:
    def __init__(self, proxy: str or None = None):
        self.__device = Applog(proxy = proxy).register_device()
        self.proxies = {'http': f'http://{proxy}', 'http': f'http://{proxy}'} if proxy else None
    
    def _base_payload(
            self, 
            extra  : str = "install", 
            slb    : str = "<N/A>", 
            hdf    : str = "<N/A>", 
            acg_m  : int =  1,
            rebuild: int = -1,
            sg_s   : int = 0,
            sign   : str = "",
        ):

        __xlog_data =  {
            "extra"  : extra,
            "grilock": "",
            "ast"    : 2,
            "p1"     : str(self.__device["device_id"]),
            "p2"     : str(self.__device["install_id"]),
            "ait"    : int(str(self.__device["install_time"])[:10]),
            "ut"     : self.__device["ut"],
            "pkg"    : "com.zhiliaoapp.musically.go",
            "prn"    : "CZL-MRP_T",
            "vc"     : 160904,
            "fp"     : f"samsung/dream2qltezh/dream2qltechn:7.1/N2G48H/{self.__device['device_serial']}ZHU1AQEE:user/release-keys",
            "vpn"    : 1,
            "hw": {
                # removed from preview
            },
            "id":{
                # removed from preview
            },
            "emulator" : {
                # removed from preview
            },
            "env" : {
                # removed from preview
            },
            "extension" : {
                # removed from preview
            },
            "paradox": {},
            "gp_ctl" : {
                "usb" : -1,
                "adb" : -1,
                "acc" : ""
            },
            "custom_info" : {},
            "hc"  : self.__device["hc"],
            "fch" : "0000000000"
        }
        
        __xlog_data["fch"] = Utils._fch(json.dumps(__xlog_data).replace(" ", ""))
        
        return Utils._xlencrypt(
            json.dumps(
                __xlog_data, separators=(",", ":")
            ).replace(" ", "")
        )
        
    def __get_headers(self, params: str, data: (str or None) = None) -> dict:
        sig = Utils._sig(
            params = params,
            body   = bytes.fromhex(data) if data is not None else None
        )
        
        headers = {
            "x-ss-stub"         : hashlib.md5(data.encode()).hexdigest().upper() if data is not None else None,
            "accept-encoding"   : "gzip",
            "cookie"            : "sessionid=",
            "x-gorgon"          : sig["X-Gorgon"],
            "x-khronos"         : sig["X-Khronos"],
            "content-type"      : "application/octet-stream" if data is not None else None, 
            "host"              : "xlog-va.byteoversea.com",
            "connection"        : "Keep-Alive",
            "user-agent"        : "okhttp/3.10.0.1"
        }
        
        return {
            key: value for key, value in headers.items() if value is not None
        }
    
    def __get_params(self) -> str:
        return urlencode(
            {
                "os"      : 0,
                "ver"     : "0.6.11.29.19-MT",
                "m"       : 2,
                "app_ver" : APP["version"],
                "region"  : "en_US",
                "aid"     : 1340,
                "did"     : self.__device['device_id'],
                "iid"     : self.__device['install_id']
            }
        )
        
    def __get_xlog(self) -> requests.Response:
        params = self.__get_params()
        
        return json.loads(
            XLEncrypt().decrypt(
                requests.get(
                    url     = "https://xlog-va.byteoversea.com/v2/s?" + params,
                    headers = self.__get_headers(params),
                    proxies = self.proxies
                ).content.hex()
            )
        )
        
    def __alert_check(self) -> bool:
            url = f"https://applog.musical.ly/service/2/app_alert_check/?iid={self.__device['install_id']}&device_id={self.__device['device_id']}&version_code={APP['version_code']}"
            headers = {
                "accept-encoding": "gzip",
                "x-ss-req-ticket": str(int(time.time() * 1000)),
                "sdk-version": "1",
                "user-agent": "okhttp/3.10.0.1",
            }

            response = requests.get(url, headers=headers, data={},proxies = self.proxies)
            
            return response.json()
    
    def __xlog_install(self) -> dict:
        __xlog_data = self._base_payload()
        __xlog_params = self.__get_params()
        self.__alert_check()
        
        return json.loads(
            XLEncrypt().decrypt(
                requests.post(
                    url     = (
                        "https://xlog-va.byteoversea.com/v2/r/?"
                            + __xlog_params
                    ),
                    data    = bytes.fromhex(__xlog_data), 
                    headers = self.__get_headers(__xlog_params, __xlog_data),
                    proxies = self.proxies
                ).content.hex()
            )
        )
    
    def __xlog_coldstart(self, num: int = 1) -> dict:
        if num == 1:
            __xlog_data = self._base_payload(
                extra = "cold_start",
                slb   = base64.b64encode("library:EpdgManager\nlibrary:SemAudioThumbnail\nlibrary:android.ext.shared\nlibrary:android.hidl.base-V1.0-java\nlibrary:android.hidl.manager-V1.0-java\nlibrary:android.net.ipsec.ike\nlibrary:android.test.base\nlibrary:android.test.mock\nlibrary:android.test.runner\nlibrary:com.android.future.usb.accessory\nlibrary:com.android.location.provider\nlibrary:com.android.media.remotedisplay\nlibrary:com.android.mediadrm.signer\nlibrary:com.google.android.gms\nlibrary:com.publicnfc\nlibrary:com.samsung.android.ibs.framework-v1\nlibrary:com.samsung.android.knox.analytics.sdk\nlibrary:com.samsung.android.knox.knoxsdk\nlibrary:com.samsung.android.nfc.rfcontrol\nlibrary:com.samsung.android.nfc.t4t\nlibrary:com.samsung.android.psitrackersdk.framework-v1\nlibrary:com.samsung.android.semtelephonesdk.framework-v1\nlibrary:com.samsung.android.spensdk.framework-v1\nlibrary:com.samsung.bbc\nlibrary:com.samsung.device.lite\nlibrary:com.sec.android.sdhmssdk.framework-v1\nlibrary:com.sec.esecomm\nlibrary:com.sec.smartcard.auth\nlibrary:imsmanager\nlibrary:javax.obex\nlibrary:org.apache.http.legacy\nlibrary:org.simalliance.openmobileapi\nlibrary:rcsopenapi\nlibrary:saiv\nlibrary:samsungkeystoreutils\nlibrary:scamera_sdk_util\nlibrary:sec_platform_library\nlibrary:secimaging\nlibrary:semextendedformat\nlibrary:semmediatranscoder\nlibrary:semsdrvideoconverter\nlibrary:sfeffect\nlibrary:stayrotation\nlibrary:vsimmanager\n".encode()).decode(),
                hdf   = base64.b64encode("feature:reqGlEsVersion=0x30002\nfeature:android.hardware.audio.low_latency\nfeature:android.hardware.audio.output\nfeature:android.hardware.biometrics.face\nfeature:android.hardware.bluetooth\nfeature:android.hardware.bluetooth_le\nfeature:android.hardware.camera\nfeature:android.hardware.camera.any\nfeature:android.hardware.camera.autofocus\nfeature:android.hardware.camera.flash\nfeature:android.hardware.camera.front\nfeature:android.hardware.faketouch\nfeature:android.hardware.fingerprint\nfeature:android.hardware.location\nfeature:android.hardware.location.gps\nfeature:android.hardware.location.network\nfeature:android.hardware.microphone\nfeature:android.hardware.nfc\nfeature:android.hardware.nfc.any\nfeature:android.hardware.nfc.hce\nfeature:android.hardware.nfc.hcef\nfeature:android.hardware.nfc.uicc\nfeature:android.hardware.opengles.aep\nfeature:android.hardware.ram.normal\nfeature:android.hardware.screen.landscape\nfeature:android.hardware.screen.portrait\nfeature:android.hardware.se.omapi.uicc\nfeature:android.hardware.sensor.accelerometer\nfeature:android.hardware.sensor.proximity\nfeature:android.hardware.sensor.stepcounter\nfeature:android.hardware.sensor.stepdetector\nfeature:android.hardware.telephony\nfeature:android.hardware.telephony.gsm\nfeature:android.hardware.telephony.ims\nfeature:android.hardware.touchscreen\nfeature:android.hardware.touchscreen.multitouch\nfeature:android.hardware.touchscreen.multitouch.distinct\nfeature:android.hardware.touchscreen.multitouch.jazzhand\nfeature:android.hardware.usb.accessory\nfeature:android.hardware.usb.host\nfeature:android.hardware.vulkan.compute\nfeature:android.hardware.vulkan.level=1\nfeature:android.hardware.vulkan.version=4198400\nfeature:android.hardware.wifi\nfeature:android.hardware.wifi.direct\nfeature:android.hardware.wifi.passpoint\nfeature:android.software.activities_on_secondary_displays\nfeature:android.software.app_enumeration\nfeature:android.software.app_widgets\nfeature:android.software.autofill\nfeature:android.software.backup\nfeature:android.software.cant_save_state\nfeature:android.software.companion_device_setup\nfeature:android.software.connectionservice\nfeature:android.software.controls\nfeature:android.software.cts\nfeature:android.software.device_admin\nfeature:android.software.file_based_encryption\nfeature:android.software.freeform_window_management\nfeature:android.software.home_screen\nfeature:android.software.incremental_delivery\nfeature:android.software.input_methods\nfeature:android.software.ipsec_tunnels\nfeature:android.software.live_wallpaper\nfeature:android.software.managed_users\nfeature:android.software.midi\nfeature:android.software.picture_in_picture\nfeature:android.software.print\nfeature:android.software.secure_lock_screen\nfeature:android.software.securely_removes_users\nfeature:android.software.sip\nfeature:android.software.sip.voip\nfeature:android.software.verified_boot\nfeature:android.software.voice_recognizers\nfeature:android.software.vulkan.deqp.level=132383489\nfeature:android.software.webview\nfeature:com.google.android.feature.ACCESSIBILITY_PRELOAD\nfeature:com.google.android.feature.RU\nfeature:com.google.android.feature.TURBO_PRELOAD\nfeature:com.nxp.mifare\nfeature:com.samsung.android.api.version.2402\nfeature:com.samsung.android.api.version.2403\nfeature:com.samsung.android.api.version.2501\nfeature:com.samsung.android.api.version.2502\nfeature:com.samsung.android.api.version.2601\nfeature:com.samsung.android.api.version.2701\nfeature:com.samsung.android.api.version.2801\nfeature:com.samsung.android.api.version.2802\nfeature:com.samsung.android.api.version.2803\nfeature:com.samsung.android.api.version.2901\nfeature:com.samsung.android.api.version.2902\nfeature:com.samsung.android.api.version.2903\nfeature:com.samsung.android.api.version.3001\nfeature:com.samsung.android.bio.face\nfeature:com.samsung.android.knox.knoxsdk\nfeature:com.samsung.android.knox.knoxsdk.api.level.33\nfeature:com.samsung.android.sdk.camera.processor\nfeature:com.samsung.android.sdk.camera.processor.effect\nfeature:com.samsung.feature.SAMSUNG_EXPERIENCE\nfeature:com.samsung.feature.audio_listenback\nfeature:com.samsung.feature.clockpack_v08\nfeature:com.samsung.feature.device_category_phone\nfeature:com.samsung.feature.galaxyfinder_v7\nfeature:com.samsung.feature.samsung_experience_mobile_lite\nfeature:com.sec.android.secimaging\nfeature:com.sec.android.smartface.smart_stay\nfeature:com.sec.feature.cocktailpanel\nfeature:com.sec.feature.fingerprint_manager_service\nfeature:com.sec.feature.motionrecognition_service\nfeature:com.sec.feature.nsflp=530\nfeature:com.sec.feature.overlaymagnifier\nfeature:com.sec.feature.saccessorymanager\nfeature:com.sec.feature.sensorhub=41\nfeature:com.sec.feature.usb_authentication\n".encode()).decode()
            )
        if num == 2:
            __xlog_data = self._base_payload(
                extra   = "cold_start",
                acg_m   = -127,
                rebuild =  0,
                sg_s    = 1 ,
                sign    = str(APP["sig_hash"]).upper()
            )

        __xlog_params = self.__get_params()
        
        return json.loads(
            XLEncrypt().decrypt(
                requests.post(
                    url     = (
                        "https://xlog-va.byteoversea.com/v2/r/?" + __xlog_params
                    ),
                    data    = bytes.fromhex(__xlog_data), 
                    headers = self.__get_headers(__xlog_params, __xlog_data),
                    proxies = self.proxies
                ).content.hex()
            )
        )

    def validate_device(self) -> bool:
        while True:
            try:

                if self.__get_xlog()['status'] == 0:
                    print(Utils.sprint("*", 1, f"xlog {Col.blue}get{Col.reset} success"))
                    pass
                
                if self.__xlog_install()['result'] == "success":
                    print(Utils.sprint("*", 2, f'xlog post {Col.blue}install{Col.reset} success'))
                    pass
                
                if self.__xlog_coldstart(1)['result'] == "success":
                    print(Utils.sprint("*", 3, f'xlog post 01 {Col.blue}"cold_start"{Col.reset} success'))
                    pass
                
                if self.__xlog_coldstart(2)['result'] == "success":
                    print(Utils.sprint("*", 4, f'xlog post 02 {Col.blue}"cold_start"{Col.reset} success'))
                    pass
                
                url = f"https://applog.musical.ly/service/2/app_alert_check/?iid={self.__device['install_id']}&device_id={self.__device['device_id']}&version_code={APP['version_code']}"
                headers = {
                    "accept-encoding": "gzip",
                    "x-ss-req-ticket": str(int(time.time())) + "000",
                    "sdk-version"    : "1",
                    "user-agent"     : "okhttp/3.10.0.1",
                }

                response = requests.get(url, headers=headers, data={}, proxies = self.proxies)

                if response.json()["data"]["is_activated"] == 1:
                    #print(Utils.sprint("*", 5, f'Device {Col.blue}activated{Col.reset} !! | Execution time: {Col.blue}{round(time.time() - START, 1)}s'))
                    return self.__device
            except Exception:
                continue

class Captcha:
    def __init__(self, did, iid):
        self.__host       = "verification-va.tiktokv.com"
        self.__device_id  = did 
        self.__install_id = iid 
        self.__cookies    = ""
        self.__client     = requests.Session()

    def __params(self):
        params = {
            "lang": "en",
            "app_name"          : "musically_go",
            "h5_sdk_version"    : "2.26.17",
            "sdk_version"       : "1.3.3-rc.7.3-bugfix",
            "iid"               : self.__install_id,
            "did"               : self.__device_id,
            "device_id"         : self.__device_id,
            "ch"                : "beta",
            "aid"               : 1340, #"1233",
            "os_type"           : 0,
            "mode"              : "",
            "tmp"               : f"{int(time.time())}{random.randint(111, 999)}",
            "platform"          : "app",
            "webdriver"         : "false",
            "verify_host"       : f"https://{self.__host}/",
            "locale"            : "en",
            "channel"           : "beta",
            "app_key"           : "",
            "vc"                : "18.2.15",
            "app_verison"       : "18.2.15",
            "session_id"        : "",
            "region"            : ["va", "US"],
            "use_native_report" : 0,
            "use_jsb_request"   : 1,
            "orientation"       : 1,
            "resolution"        : ["900*1552", "900*1600"],
            "os_version"        : ["25", "7.1.2"],
            "device_brand"      : "samsung",
            "device_model"      : "SM-G973N",
            "os_name"           : "Android",
            "challenge_code"    : 1105,
            "app_version"       : "18.2.15",
            "subtype"           : "",
        }

        return urlencode(params)

    def __headers(self) -> dict:

        headers = {
            "sdk-version"         : "2",
            "x-ss-req-ticket"     : str(int(time.time() * 1000)),
            "cookie"              : self.__cookies,
            "content-type"        : "application/json; charset=utf-8",
            "host"                : self.__host,
            "connection"          : "Keep-Alive",
            "user-agent"          : "okhttp/3.10.0.1",
            "passport-sdk-version": "19",
        }

        return headers

    def __get_challenge(self) -> dict:

        params = self.__params()

        req = self.__client.get(
            url = (
                "https://"
                    + self.__host
                    + "/captcha/get?"
                    + params
            ),
            headers = self.__headers()
        )

        return req.json()

    def __solve_captcha(self, url_1: str, url_2: str) -> dict:
        puzzle = base64.b64encode(
            self.__client.get(
                url_1,
            ).content
        )
        piece = base64.b64encode(
            self.__client.get(
                url_2,
            ).content
        )
        
        solver = PuzzleSolver(puzzle, piece)
        maxloc = solver.get_position()
        randlength = round(
            random.random() * (100 - 50) + 50
        )
        time.sleep(1)
        return {
            "maxloc": maxloc,
            "randlenght": randlength
        }

    def __post_captcha(self, solve: dict) -> dict:
        params = self.__params()

        body = {
            "modified_img_width": 552,
            "id": solve["id"],
            "mode": "slide",
            "reply": list(
                {
                    "relative_time": i * solve["randlenght"],
                    "x": round(
                        solve["maxloc"] / (solve["randlenght"] / (i + 1))
                    ),
                    "y": solve["tip"],
                }
                for i in range(
                    solve["randlenght"]
                )
            ),
        }

        headers = self.__headers()

        req = self.__client.post(
            url = (
                "https://"
                    + self.__host
                    + "/captcha/verify?"
                    + params
            ),
            headers = headers.update(
                    {
                        "content-type": "application/json"
                }
            ),
            json = body
        )

        return req.json()

    def solve_captcha(self):
        __captcha_challenge = self.__get_challenge()

        __captcha_id = __captcha_challenge["data"]["id"]
        __tip_y = __captcha_challenge["data"]["question"]["tip_y"]

        solve = self.__solve_captcha(
            __captcha_challenge["data"]["question"]["url1"],
            __captcha_challenge["data"]["question"]["url2"],
        )
        
        solve.update(
                {
                    "id": __captcha_id,
                    "tip": __tip_y
            }
        )
        
        return self.__post_captcha(solve)
