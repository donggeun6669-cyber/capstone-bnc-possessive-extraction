# 코랩 노트북(notebook/)의 셀을 함수별로 나눈 파일. 함수 본문은 노트북과 같다.
from preprocess import read_bnc_tagged, read_noun_list
from extract import (
    extract_noun_examples,
    extract_possessive_examples,
    extract_s_possessive_examples,
    extract_of_examples,
    extract_whose_examples,
)
from save import save_noun_examples

# 프롬프트 9로 Codex(GPT-6.1 Sol High)가 생성한 코드
import json
from pathlib import Path


def main(
    corpus_filename="/content/bnc_tagged.txt",
    noun_filename="/content/noun_list.txt"
):
    output_folder = Path("output")
    output_folder.mkdir(parents=True, exist_ok=True)

    # 1. 코퍼스와 명사 목록 전처리
    corpus_data = read_bnc_tagged(corpus_filename)
    noun_dictionary = read_noun_list(noun_filename)

    # 2. 문장 ID와 문장 텍스트를 리스트로 저장
    corpus_text_data = [
        (sentence_id, " ".join(token[0] for token in tokens))
        for sentence_id, tokens in corpus_data
    ]

    with (output_folder / "bnc_corpus_data.txt").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(corpus_text_data, f, ensure_ascii=False, indent=2)

    # 3. 용례를 추가하기 전의 명사 딕셔너리 저장
    with (output_folder / "noun_dictionary.txt").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(noun_dictionary, f, ensure_ascii=False, indent=2)

    # 문장 텍스트 저장용 임시 리스트의 메모리 해제
    del corpus_text_data

    # 4. 유형별 추출 함수 지정
    extractors = [
        ("all", extract_noun_examples),
        ("pron", extract_possessive_examples),
        ("s", extract_s_possessive_examples),
        ("of", extract_of_examples),
        ("whose", extract_whose_examples),
    ]

    # 5. 유형마다 새 명사 딕셔너리로 추출하고 저장
    for example_type, extractor in extractors:
        fresh_noun_dictionary = read_noun_list(noun_filename)
        noun_examples = extractor(corpus_data, fresh_noun_dictionary)

        save_noun_examples(
            noun_examples_dict=noun_examples,
            folder=str(output_folder),
            header="bnc",
            type=example_type
        )

        print(f"{example_type} 용례 및 빈도수 파일 저장 완료")

    print(f"총 12개 파일 저장 완료: {output_folder.resolve()}")


# 실행
if __name__ == "__main__":
    main(
        corpus_filename="data/bnc_tagged.txt",
        noun_filename="data/noun_list.txt"
    )
