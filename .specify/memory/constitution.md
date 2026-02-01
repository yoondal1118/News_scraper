<!--
Sync Impact Report
- Version: N/A -> 1.0.0
- Modified principles: N/A (initial constitution)
- Added sections: Core Principles, 추가 제약사항, 개발 워크플로우 & 품질 게이트, Governance
- Removed sections: 없음
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md
	- ✅ .specify/templates/tasks-template.md
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): 최초 비준 일자가 확인되지 않아 추후 확정 필요
-->

# 네이버 뉴스 스크래퍼 및 다이어리 헌법

## Core Principles

### I. 테스트 우선 (Pytest, 비협상 원칙)
모든 기능 변경은 반드시 Pytest 테스트를 먼저 작성한다. 테스트는 사용자 승인
후에 실행하며, 실패(RED) 상태를 확인한 뒤에만 구현을 진행한다. 리팩터링은
GREEN 상태에서만 수행한다. 테스트 없는 구현은 금지한다.

### II. HITL 승인 게이트
각 단계(요구사항/계획/테스트 작성/구현/검증/릴리스)마다 사용자 승인 없이
다음 단계로 진행할 수 없다. 승인 요청은 변경 요약, 영향 범위, 검증 계획을
포함해야 한다.

### III. 한국어 명세 일관성
모든 명세서와 설명(스펙, 계획, 작업 목록, 연구 메모, 문서)은 한국어로만
작성한다. 자동 생성 템플릿도 한국어를 기본으로 유지한다.

### IV. 캘린더 UI 미학 규정
캘린더 UI는 2026년 트렌드인 Glassmorphism과 Bento Grid를 적용한 세련된
레이아웃을 반드시 따른다. UI 아이콘/이모지는 윈도우 이모지를 사용하지
않고, emoji 라이브러리를 사용한다.

### V. 작업 범위 고정
모든 작업은 C:\code\news_scraper 폴더 내에서만 수행한다. 외부 경로에 대한
읽기/쓰기/실행을 금지한다.

## 추가 제약사항

- 본 프로젝트는 네이버 뉴스 스크래퍼 및 다이어리 기능을 대상으로 한다.
- 테스트 프레임워크는 Pytest를 기본 표준으로 사용한다.
- UI 구현 시 Glassmorphism(반투명, 블러, 라이트 보더)과 Bento Grid
	(모듈형 카드, 균형 잡힌 여백) 원칙을 준수한다.

## 개발 워크플로우 & 품질 게이트

1. **요구사항 정리**: 한국어로 작성하고 사용자 승인 필요.
2. **테스트 작성**: Pytest로 테스트 먼저 작성 → 승인 요청.
3. **테스트 실행**: 실패(RED) 확인 후 기록.
4. **구현**: 승인된 테스트를 통과하도록 최소 구현.
5. **리팩터링**: 테스트 GREEN 상태에서만 수행.
6. **검증**: 테스트 결과와 변경 요약을 사용자에게 보고.
7. **다음 단계 진행**: 사용자 승인 후에만 가능.

## Governance

- 본 헌법은 모든 프로젝트 관행보다 우선한다.
- 모든 리뷰는 헌법 준수 여부를 반드시 확인해야 한다.
- 개정은 변경 사유, 영향 분석, 이행 계획을 문서화하고 사용자 승인을
	받아야 한다.
- 버전 규칙은 SemVer(주.부.수)를 따른다.
	- MAJOR: 원칙 삭제/핵심 의미 변경
	- MINOR: 원칙/섹션 추가 또는 실질적 확장
	- PATCH: 문구 정정, 명확화, 오탈자 수정
- 컴플라이언스 점검은 계획 단계와 구현 완료 시점에 각각 수행한다.

**Version**: 1.0.0 | **Ratified**: 2026-01-29 | **Last Amended**: 2026-01-29
