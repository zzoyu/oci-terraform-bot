import subprocess
import time
import re
import requests
import os
from sys import exit
from dotenv import load_dotenv

load_dotenv()

# 환경변수 설정
RETRYABLE_PATTERNS = os.getenv(
    "RETRYABLE_PATTERNS"
).split(",")  # Retryable patterns for Terraform errors
RETRY_DELAY_SECONDS = os.getenv(
    "RETRY_DELAY_SECONDS"
)  # Default delay is 60 seconds
DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)  # Add your Discord webhook URL here
DISCORD_USERNAME = os.getenv(
    "DISCORD_USERNAME"
)  # Default username for Discord bot
YOUR_NAME = os.getenv("YOUR_NAME")

def run_terraform_apply():
    try:
        result = subprocess.run(
            ["terraform", "apply", "-auto-approve", "-no-color", "-compact-warnings"],
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        return result.returncode, output
    except Exception as e:
        return 1, str(e)


def is_retryable_error(output):
    retryable_patterns = RETRYABLE_PATTERNS
    return any(
        re.search(pattern, output, re.IGNORECASE) for pattern in retryable_patterns
    )


def send_discord_notification(
    webhook_url, message, embed=None, username=DISCORD_USERNAME
):
    # Discord 메시지 전송
    print(
        requests.request(
            method="POST",
            url=webhook_url,
            json={"content": message, "username": username, "embeds": embed},
        ).text
    )


def main():
    if not DISCORD_WEBHOOK_URL:
        print("❌ Discord Webhook URL이 설정되지 않았습니다.")
        exit(1)

    print("🔄 Terraform apply 시작...")
    attempt = 1

    try:
        while True:
            print(f"🚀 Attempt {attempt}...")
            attempt += 1

            code, output = run_terraform_apply()

            temp = ""
            for line in output.splitlines():
                if line is not None and line.strip() != "":
                    temp += line + "\n"
            temp = temp.splitlines()

            # Terraform 실행 결과의 끝에서 10줄만 추출
            condensed_output = temp[-10:]

            if code == 0:
                print("✅ Terraform apply succeeded!")

                # Discord 메시지 전송
                send_discord_notification(
                    DISCORD_WEBHOOK_URL,
                    message=f"# Terraform Apply 성공! 🎉\n## 총 {attempt} 회 시도 끝에 생성했습니다! Tlqkf",
                    embed=[{
                        "title": "Terraform Apply Output",
                        "description": "\n".join(condensed_output),
                        "color": 3066993,
                    }],
                )
                break
            elif is_retryable_error(output):
                if attempt % 100 == 0:
                    send_discord_notification(
                        DISCORD_WEBHOOK_URL,
                        message=f"## 오라클 서버 존버 지금까지 {attempt}회째 시도 중... 🚀\n_**진건이의 도전은 계속된다**_",
                    )
                print("⚠️  Retryable error detected. Retrying after delay...")
                time.sleep(float(RETRY_DELAY_SECONDS))
            else:
                print("❌ Non-retryable error. Exiting.")
                print(output)
                break
    except KeyboardInterrupt:
        print("🛑 User interrupted the process.")
    except Exception as e:
        print(f"💀 An unexpected error occurred: {e}")
        send_discord_notification(
            webhook_url=DISCORD_WEBHOOK_URL,
            message=f"# 뭔가 오류났다 {YOUR_NAME}아!! 💀",
            embed=[
                {
                    "title": "Terraform Apply Output",
                    "description": "\n".join(condensed_output),
                    "color": 16711680,
                }
            ],
            username=DISCORD_USERNAME,
        )
    finally:
        print("🔚 Terraform apply process ended.")


if __name__ == "__main__":
    main()
