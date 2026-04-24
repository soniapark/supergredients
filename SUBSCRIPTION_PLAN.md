# Supergredients 구독 서비스 계획

## 개요

클린푸드 성분 분석 서비스를 유료 구독 모델로 전환하기 위한 계획서

---

## 1. 결제 시스템 선택

### 추천: Stripe

| 항목 | Stripe | Toss Payments | 기타 |
|------|--------|---------------|------|
| 해외 결제 | O | X | - |
| 구독 관리 | 내장 | 별도 구현 | - |
| GitHub Pages 연동 | 쉬움 | 복잡 | - |
| 수수료 | 2.9% + 30¢ | 2.5~3.5% | - |
| 한국 원화 | O | O | - |

**선택 이유**:
- Client-side에서 바로 결제 가능 (Stripe Checkout)
- 별도 백엔드 서버 불필요
- 구독 자동 갱신 내장

---

## 2. 가격 플랜 (제안)

### Free 플랜
- 제품 검색: 무제한
- 클린 스코어 확인: 10회/일
- OCR 분석: 3회/일
- Claude AI 분석: X (본인 API 키로 가능)

### Pro 플랜 - ₩9,900/월
- 제품 검색: 무제한
- 클린 스코어 확인: 무제한
- OCR 분석: 50회/일
- Claude AI 분석: 30회/일 (내장 API)
- 신제품 알림
- 광고 제거

### Team 플랜 - ₩29,900/월
- Pro 기능 전체
- 팀원 5명
- API 접근
- 맞춤 리포트

---

## 3. 필요한 사용자 작업

### 3.1 Stripe 계정 설정 (필수)

1. **Stripe 가입**: https://dashboard.stripe.com/register
2. **사업자 인증**: 개인/사업자 정보 입력
3. **API 키 발급**:
   - Dashboard → Developers → API keys
   - Publishable key (공개용) 복사
   - Secret key (비공개) - 백엔드용, GitHub Pages에선 사용 안함

4. **제품 생성**:
   - Dashboard → Products → Add product
   - "Supergredients Pro" 생성
   - Price: ₩9,900, Recurring monthly

5. **결제 링크 생성**:
   - Dashboard → Payment Links → Create
   - 생성된 링크를 pricing.html에 연결

### 3.2 환경 변수 (선택 - 고급)

GitHub Pages는 환경 변수를 지원하지 않음.
대안:
- Stripe Checkout Link 직접 사용 (권장)
- Netlify/Vercel로 마이그레이션

---

## 4. 구현 코드

### 4.1 pricing.html 추가

```html
<!-- pricing.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>가격 - Supergredients</title>
    <script src="https://js.stripe.com/v3/"></script>
    <style>
        /* 스타일은 index.html에서 복사 */
    </style>
</head>
<body>
    <div class="pricing-container">
        <div class="plan free">
            <h3>Free</h3>
            <p class="price">₩0</p>
            <ul>
                <li>제품 검색 무제한</li>
                <li>클린 스코어 10회/일</li>
                <li>OCR 분석 3회/일</li>
            </ul>
            <a href="index.html" class="btn">시작하기</a>
        </div>

        <div class="plan pro featured">
            <h3>Pro</h3>
            <p class="price">₩9,900<span>/월</span></p>
            <ul>
                <li>모든 기능 무제한</li>
                <li>Claude AI 분석 30회/일</li>
                <li>신제품 알림</li>
                <li>광고 제거</li>
            </ul>
            <!-- Stripe Payment Link로 교체 -->
            <a href="https://buy.stripe.com/YOUR_PAYMENT_LINK" class="btn btn-primary">구독하기</a>
        </div>
    </div>
</body>
</html>
```

### 4.2 구독 상태 확인 (localStorage 기반 - 간단 버전)

```javascript
// 결제 완료 후 success 페이지에서 실행
function activateSubscription() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('success') === 'true') {
        localStorage.setItem('subscription', JSON.stringify({
            plan: 'pro',
            activatedAt: new Date().toISOString(),
            // 실제로는 Stripe webhook으로 검증 필요
        }));
    }
}

// 기능 사용 시 체크
function checkSubscription() {
    const sub = JSON.parse(localStorage.getItem('subscription') || '{}');
    return sub.plan === 'pro';
}
```

---

## 5. 보안 고려사항

### GitHub Pages 한계

- **백엔드 없음**: Webhook 수신 불가
- **API 키 노출**: Secret key 사용 불가
- **구독 검증**: Client-side만 가능 (우회 가능)

### 권장 솔루션

**Level 1 (현재 - 간단)**:
- Stripe Payment Link 사용
- localStorage로 구독 상태 저장
- 우회 가능하지만 대부분 사용자는 정상 결제

**Level 2 (권장 - 중기)**:
- Netlify/Vercel로 마이그레이션
- Serverless Function으로 Stripe Webhook 처리
- 구독 상태 서버에서 검증

**Level 3 (장기)**:
- 별도 백엔드 서버 (Node.js/Python)
- 사용자 인증 시스템
- 완전한 구독 관리

---

## 6. 다음 단계

### 사용자가 해야 할 일

1. [ ] Stripe 계정 생성
2. [ ] 제품/가격 플랜 생성
3. [ ] Payment Link 생성
4. [ ] pricing.html 파일에 링크 추가
5. [ ] success.html 결제 완료 페이지 생성
6. [ ] 테스트 결제 진행

### Claude가 도와줄 수 있는 것

- [ ] pricing.html 전체 페이지 작성
- [ ] success.html 페이지 작성
- [ ] 구독 상태 체크 로직 index.html에 추가
- [ ] 무료/유료 기능 분리 구현

---

## 7. 타임라인 (제안)

| 단계 | 작업 | 소요 시간 |
|------|------|----------|
| 1 | Stripe 계정 설정 | 30분 |
| 2 | 제품/가격 생성 | 15분 |
| 3 | Payment Link 생성 | 10분 |
| 4 | pricing.html 추가 | 1시간 (Claude 지원) |
| 5 | 기능 제한 구현 | 2시간 (Claude 지원) |
| 6 | 테스트 | 30분 |

**총 예상 시간**: 4-5시간

---

*작성일: 2026-01-31*
