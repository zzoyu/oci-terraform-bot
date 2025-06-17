# OCI terraform automation bot

## Introdution

- Python 3.13
- Terraform 1.11.4

Terraform을 사용하여 모 클라우드 서비스에 프리 티어 인스턴스를 생성하고, Discord를 통해 알림을 보내주는 간단한 스크립트입니다.
성공할 때까지 계속 시도하며, `Ctrl+C` 등으로 종료가 가능합니다. 메시지 내용은 편의상 변경하지 않았습니다.
메시지를 보내는 기준은 다음과 같습니다.

- 생성 성공
- 리전 내 공간 부족 외 다른 오류 발생
- 100회 단위로 알림

그 외 민감한 정보는 환경변수로 관리합니다.

## 구조

세팅이 완료된 후의 구조는 아래와 같습니다.

```zsh
├── .git
├── .terraform
├── .venv
├── .DS_Store
├── .env
├── .env.example
├── .gitignore
├── README.md
├── [YOUR TERRAFORM SCRIPT].tf
├── naenwa.py
├── requirements.txt
└── terraform.tfstate
```

## 사용법

### 1. 환경변수 설정

환경변수는 `.env` 파일에 작성합니다. 예제는 `.env.example`를 참고하시기 바랍니다.

```env
DISCORD_WEBHOOK_URL=<YOUR DISCORD WEBHOOK URL>
DISCORD_USERNAME=<DISCORD BOT USERNAME>
RETRY_DELAY_SECONDS=<RETRY DELAY IN SECONDS>
RETRYABLE_PATTERNS=<ERROR PATTERNS TO RETRY>
YOUR_NAME=<YOUR NAME>
```

### 2. API 키 설정

OCI 콘솔 페이지에서 사용자의 API 키를 발급합니다.
키를 발급받을 때 표시되는 값과 키는 잘 보관합니다.

### 3. Terraform 설정

> Terraform 스크립트 내부 인스턴스 관련 설정은 생략합니다.

클라우드 서비스 환경에 맞게 작성해주세요. 인스턴스 생성 스택에서 `provider` 부분이 삭제된 스크립트를 얻을 수 있습니다.
`provider`블록은 스택 실행 시 표시되는 로그를 참고하여 작성합니다. 숨겨진 필드는 2번에서 앞서 발급받은 정보로 작성할 수 있습니다.
이후 `terraform init`을 통해 초기화합니다. `terraform apply`를 실행하여 정상적으로 요청이 발생하는지 확인합니다. 50x에러가 발생하는 경우 봇을 가동할 준비가 되었습니다.

### 4. python 실행

`.venv`를 사용하여 가상환경을 생성하는 것을 권장합니다.
`requirements.txt`의 패키지들을 설치한 후 실행합니다.

```bash
python naenwa.py
```

## Disclaimer

- 본 코드는 개인적인 용도로 작성된 것입니다.
- 수정 시 인프라 정보나 키 등 민감한 정보를 푸시하지 않도록 주의하세요.
