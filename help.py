# FastAPI 서버 실행하기 (백엔드 서버)
# uvicorn main:app --reload

# Svelte 서버 실행하기 (프론트엔드 서버)
# frontend 디렉토리에서
# npm run dev

# 모델(models.py) 변경 시 alembic 명령어
# alembic revision --autogenerate
# alembic upgrade head

# 서버 접속
# ssh -i ~/myapi.pem ubuntu@15.165.82.55
# 이후 가상환경 진입
# myapi

# (안씀) FastAPI 서버 실행하기 / 꼭 프로젝트 파일에서 (venvs 파일 아님)
# uvicorn main:app --reload --host=0.0.0.0

# (안씀) gunicorn 시작/ 종료: stop/ 재시작: restart
# sudo systemctl start myapi.service

# nginx 시작: 8000 필요없음
# sudo systemctl start nginx
# sudo nano /etc/nginx/sites-available/myapi 명령으로 수정할 수 있다.
# 서버 로그 확인하기
# tail -f myapi.log

