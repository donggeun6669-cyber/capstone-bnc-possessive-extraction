# 코랩 노트북(notebook/)의 셀을 함수별로 나눈 파일. 함수 본문은 노트북과 같다.

# 프롬프트 8로 Codex(GPT-6.1 Sol High)가 생성한 코드
from pathlib import Path


def save_noun_examples(noun_examples_dict, folder, header, type):
    output_folder = Path(folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    count_path = output_folder / f"{header}_noun_{type}_count.txt"
    examples_path = output_folder / f"{header}_noun_{type}.txt"

    with (
        count_path.open("w", encoding="utf-8") as count_file,
        examples_path.open("w", encoding="utf-8") as examples_file
    ):
        for noun, examples in noun_examples_dict.items():
            if not examples:
                continue

            # 튜플 전체를 기준으로 중복 제거, 처음 등장한 순서 유지
            unique_examples = list(dict.fromkeys(examples))

            # 빈도수 파일: 명사, 중복 제거한 용례 수, 첫 번째 예문
            first_sentence = unique_examples[0][2]
            count_file.write(
                f"{noun}\t{len(unique_examples)}\t{first_sentence}\n"
            )

            # 용례 파일: 명사, 문장 ID, 소유자 단어, 전체 문장
            for sentence_id, owner, sentence in examples:
                examples_file.write(
                    f"{noun}\t{sentence_id}\t{owner}\t{sentence}\n"
                )

    return str(count_path), str(examples_path)
