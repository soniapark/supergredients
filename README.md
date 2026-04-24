# Supergredients

클린푸드 성분 분석 및 제품 검색 서비스

## 배포 방법

### 1. GitHub Repository 생성

```bash
# 새 repository 생성 후
cd github-deploy
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/supergredients.git
git push -u origin main
```

### 2. GitHub Pages 활성화

1. Repository Settings → Pages
2. Source: "GitHub Actions" 선택
3. 자동으로 `.github/workflows/deploy.yml` 실행됨

### 3. 커스텀 도메인 (선택)

1. Settings → Pages → Custom domain
2. `supergredients.com` 또는 원하는 도메인 입력
3. DNS 설정에서 CNAME 레코드 추가

## 파일 구조

```
/
├── index.html      # 메인 페이지 (SPA)
├── products.json   # 제품 데이터베이스
├── logo.png        # 로고 이미지
├── README.md       # 이 파일
└── .github/
    └── workflows/
        └── deploy.yml  # GitHub Actions 배포 설정
```

## 기능

- 제품 검색 및 필터링
- 클린 스코어 분석 (CLEAN/OK/NO)
- OCR 성분 분석 (Tesseract.js)
- Claude AI 성분 분석 (사용자 API 키 필요)
- 제휴 링크 (Oasis, Coupang, Kurly)

## 구독 서비스 연동 (TODO)

결제 연동을 위해 다음 작업 필요:

1. **Stripe 계정 생성**: https://stripe.com
2. **가격 플랜 설정**: Stripe Dashboard에서 Products 생성
3. **결제 페이지 추가**: pricing.html, checkout flow
4. **Webhook 설정**: 결제 완료 후 처리

상세 계획: `SUBSCRIPTION_PLAN.md` 참조
