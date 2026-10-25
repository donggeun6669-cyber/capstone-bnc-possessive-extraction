# 코랩 노트북(notebook/)의 셀을 함수별로 나눈 파일. 함수 본문은 노트북과 같다.

# 프롬프트 1로 Codex(GPT-6.1 Sol High)가 생성한 코드
import re


def read_bnc_tagged(filename="/content/bnc_tagged.txt"):
    results = []
    tokens = []
    last_id = None
    current_id = None
    sequence = 1
    missing_start_count = 0

    start_pattern = re.compile(r"""<s\s+id\s*=\s*["']?(\d+)["']?\s*>""")

    with open(filename, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\r\n")
            tag = line.strip()

            # 시작 태그에서 숫자 ID 추출
            match = start_pattern.fullmatch(tag)
            if match:
                last_id = match.group(1)
                current_id = last_id
                sequence = 1
                continue

            # 종료 태그를 만나면 문장 저장
            if tag == "</s>":
                if current_id is None:
                    if last_id is None:
                        raise ValueError(
                            "첫 문장에 시작 태그가 없어 기준 ID를 정할 수 없습니다."
                        )

                    sequence += 1
                    current_id = f"{last_id}-{sequence}"
                    missing_start_count += 1

                results.append((current_id, tokens))
                tokens = []
                current_id = None
                continue

            # 정확히 7개 필드인 토큰만 저장
            fields = line.split("\t")
            if len(fields) == 7:
                tokens.append(fields)

    print(f"전체 문장 수: {len(results)}")
    print(f"시작 태그가 없던 문장 수: {missing_start_count}")

    return results


# 프롬프트 2로 Codex(GPT-6.1 Sol High)가 생성한 코드
def read_noun_list(filename="/content/noun_list.txt"):
    noun_list = {}

    with open(filename, "r", encoding="utf-8-sig") as f:
        for line in f:
            if not line.strip():
                continue

            lemma = line.split("\t")[0].strip().lower()
            noun_list[lemma] = []

    return noun_list
