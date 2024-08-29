# fastApi 스터디

- [x] CRUD
- [ ] PyTest
- [ ] JWT
- [ ] OAuth2

# Requiremnets

```
python -m venv .venv # 3.10
pip install -r requirements.txt
```

# MVC Structure

- controller
  - login_controller
    - 회원가입
    - 로그인 JWT > OAuth2
    - 회원정보 관리
  - user_controller
    - CRUD 테스트
    - 사용자 목록
- service
  - main_service
  - user_service
- models
  - user_model
- auth
  - JWT 관련, 정리 필요
- db
  - mysql db 연결정보
- error
  - 에러 핸들링
- main
  - app config

# 프로젝트 구조

- fast-auth
  - host, 나중에 도커로 변경
- mysql
  - 도커
