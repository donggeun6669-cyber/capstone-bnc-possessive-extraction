# BNC 소유 구문 용례 데이터 추출

인공지능과 영어학 캡스톤 중간과제 (2026-2, 성균관대학교) · 2023313955 정동근

의존구조 파싱이 된 BNC에서 영어 소유 구문의 용례를 뽑는 코드이다. 바이브 코딩과 컨텍스트 엔지니어링으로 Codex에게 함수를 하나씩 요청해 만들었다.

## 추출 대상

- 명사 50개: Haspelmath(2008a: 19; 2017: 204–205)의 명사 목록 (친족어 15, 신체 부위어 16, 양도 가능 명사 19) → [`data/noun_list.txt`](data/noun_list.txt)
- 구문 4가지
  - ① 대명사 소유 (his face)
  - ② ’s 소유격 (John’s face)
  - ③ of 구문 (the face of the man)
  - ④ whose 소유 (the man whose face)

## 폴더

| 폴더 | 내용 |
|---|---|
| [`notebook/`](notebook/) | 코랩에서 실행한 노트북 원본 (제출한 것 그대로) |
| [`src/`](src/) | 노트북 코드를 함수별 파일로 나눈 것. 함수 본문은 노트북과 같다 |
| [`prompts/`](prompts/prompts.md) | Codex에 넣은 프롬프트 1–9 |
| [`data/`](data/) | 명사 목록. BNC 파일은 넣지 않았다 |

`src/` 파일과 프롬프트의 관계

| 파일 | 프롬프트 | 하는 일 |
|---|---|---|
| `preprocess.py` | 1, 2 | 코퍼스 읽기, 명사 목록 읽기 |
| `extract.py` | 3–7 | 전체 용례와 ①–④ 용례 추출 |
| `save.py` | 8 | 빈도수 파일과 용례 파일 저장 |
| `main.py` | 9 | 전체 실행 |

## 실행

1. 수업에서 받은 `bnc_tagged.txt`를 `data/`에 넣는다. (BNC는 재배포하지 않는다)
2. 저장소 맨 위 폴더에서 실행한다.

```bash
python3 src/main.py
```

`output/`에 파일 12개(유형별 용례 파일 5개, 빈도수 파일 5개, 전처리 결과 2개)가 생긴다.

## 결과

| 유형 | 용례 수 | 중복 제거 후 | 용례가 있는 명사 |
|---|---:|---:|---:|
| 전체 (목록 명사가 NOUN으로 쓰인 경우) | 20,555 | 19,606 | 50 |
| ① 대명사 소유 | 7,738 | 7,631 | 50 |
| ② ’s 소유격 | 953 | 952 | 48 |
| ③ of 구문 | 726 | 718 | 44 |
| ④ whose 소유 | 44 | 44 | 19 |

- 코퍼스는 94,171문장이고, 그중 2,598문장은 시작 줄(`<s id=…>`) 없이 시작한다.
- `src/`로 다시 실행한 결과 파일 12개는 코랩 결과와 내용이 같다.

## AI 활용

- 코드: Codex(GPT-6.1 Sol High)가 프롬프트 1–9로 생성했다. 셀과 파일마다 주석으로 표시했다.
- 프롬프트 4–7은 첫 실행에서 용례를 찾지 못해, 같은 대화창에서 한 번 수정을 요청했다.
- Claude Code(Claude Opus 5.5)는 논문 검색, 코랩 실행 결과 점검, 프롬프트 초안, 코드 점검에 썼다.

## 참고문헌

- Haspelmath, M. (2008a). Frequency vs. iconicity in explaining grammatical asymmetries. *Cognitive Linguistics*, 19(1), 1–33.
- Haspelmath, M. (2017). Explaining alienability contrasts in adpossessive constructions: Predictability vs. iconicity. *Zeitschrift für Sprachwissenschaft*, 36(2), 193–231.
