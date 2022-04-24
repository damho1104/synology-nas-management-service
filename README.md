# Synology NAS Management Service
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fdamho1104%2Fsynology-nas-management-service&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Github&edge_flat=false)](https://hits.seeyoufarm.com)
![Python](https://img.shields.io/badge/Python-3776AB.svg?&style=flat&logo=Python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)  
로컬망에서 Synology NAS 관리용 API 를 제공하는 FastAPI 기반 서비스 입니다.   

## Release
### v1.0.0
- Synology NAS 제품군 종료 API 추가
- Synology NAS 제품군 켜기 API 추가 (WOL, Wake On Lan)
- 비동기 지원

## 1. config.json 생성
- 서버를 실행시킬 host ip 와 port 정보를 입력합니다.
- Synology NAS 제품군 정보를 입력합니다.
```text
{
  "ip": "[HOST_IP_FOR_LAUNCH_SERVICE]",
  "port": "[HOST_PORT_FOR_LAUNCH_SERVICE]",
  "servers": {
    "[SYNOLOGY_NAS_NAME]": {
      "ip": "[SYNOLOGY_NAS_IP]",
      "port": "[SYNOLOGY_NAS_WEB_MANAGEMENT_PORT]",
      "id": "[SYNOLOGY_NAS_ID_FOR_ADMIN]",
      "pw": "[SYNOLOGY_NAS_PASSWORD_FOR_ADMIN]",
      "dsm_major_version": [SYNOLOGY_NAS_MAJOR_VERSION]
    },
    "[OTHER_SYNOLOGY_NAS_NAME]": {
      "ip": "[SYNOLOGY_NAS_IP]",
      "port": "[SYNOLOGY_NAS_WEB_MANAGEMENT_PORT]",
      "id": "[SYNOLOGY_NAS_ID_FOR_ADMIN]",
      "pw": "[SYNOLOGY_NAS_PASSWORD_FOR_ADMIN]",
      "dsm_major_version": [SYNOLOGY_NAS_MAJOR_VERSION]
    },
    ...
  },
  "ip_whitelist": [
    "[CLIENT_IP]"
  ]
}
```

### Example
#### Case 1. Synology NAS 로컬 서버(192.168.0.3, 5000, DSM Version: 6.2.3) 가 1대인 경우
- Host Info: 192.168.0.100, 10000
```json
{
  "ip": "192.168.0.100",
  "port": "10000",
  "server": {
    "MYNAS1": {
      "ip": "192.168.0.3",
      "port": "5000",
      "mac": "00:11:22:33:44:55",
      "id": "admin",
      "pw": "adminadmin",
      "dsm_major_version": 6
    }
  },
  "ip_whitelist": [
    "192.168.0.3",
    "192.168.0.4",
    "192.168.0.5"
  ]
}
```

#### Case 2. Synology NAS 로컬 서버(192.168.0.3, 5000, DSM Version: 6.2.3) 가 2대인 경우
```text
Host 정보
192.168.0.100, 10000

Synology NAS 로컬 서버 정보
1. MYNAS1, 192.168.0.3, 5000, DSM Version: 6.2.3
2. MYNAS2, 192.168.0.13, 5000, DSM Version: 7.0.1
```
```json
{
  "ip": "192.168.0.100",
  "port": "10000",
  "server": {
    "MYNAS1": {
      "ip": "192.168.0.3",
      "port": "5000",
      "mac": "00:11:22:33:44:55",
      "id": "admin",
      "pw": "adminadmin",
      "dsm_major_version": 6
    },
    "MYNAS2": {
      "ip": "192.168.0.13",
      "port": "5000",
      "mac": "AA:00:22:33:44:AF",
      "id": "admin",
      "pw": "adminadmin",
      "dsm_major_version": 7
    }
  },
  "ip_whitelist": [
    "192.168.0.3",
    "192.168.0.4",
    "192.168.0.5"
  ]
}
```


## 2. 실행
### 1. Windows OS
- pmws-v1.0.0.zip 압축 파일을 다운로드 받습니다.
- 다운로드 받은 파일의 압축을 풀고 파일이 위치하는 곳에서 cmd 창을 켜서 아래와 같은 방법으로 실행합니다.
```shell
> cd [압축 푼 디렉토리 경로]
> syno-manage-server.exe
```
### 2. Others
- Python 3.9 기반에서 작성되었습니다.
- 해당 프로젝트를 clone 후 디렉토리로 이동합니다.
- 패키지를 다운로드 받습니다.
  ```shell
  $ pip3 install -r requirements.txt
  ```
- 이후부터는 case 1 혹은 2 를 수행하시면 됩니다.
#### Case 1. Build
- 아래 명령과 같이 실행합니다.
  ```shell
  $ pyinstaller server.spec
  ```
- dist 디렉토리로 이동하여 아래 명령과 같이 실행합니다.
  ```shell
  $ ./syno-manage-server
  ```
#### Case 2. Run script
- 아래 명령과 같이 실행합니다.
  ```shell
  $ python3 src/server.py
  ```