# 코랩 노트북(notebook/)의 셀을 함수별로 나눈 파일. 함수 본문은 노트북과 같다.

# 프롬프트 3으로 Codex(GPT-6.1 Sol High)가 생성한 코드
def extract_noun_examples(corpus_data, noun_list):
    for sentence_id, tokens in corpus_data:
        sentence_text = " ".join(token[0] for token in tokens)

        for token in tokens:
            lemma = token[2].lower()
            upos = token[1]

            if upos == "NOUN" and lemma in noun_list:
                noun_list[lemma].append(
                    (sentence_id, "-", sentence_text)
                )

    return noun_list


# 프롬프트 4,5,6,7을 수정해 Codex(GPT-6.1 Sol High)가 다시 생성한 코드
def extract_possessive_examples(corpus_data, noun_list):
    possessives = {"my", "your", "his", "her", "its", "our", "their"}

    for sentence_id, tokens in corpus_data:
        sentence_text = " ".join(token[0] for token in tokens)

        # 핵어 ID별로 의존소를 모음
        dependents = {}
        for token in tokens:
            dependents.setdefault(token[4], []).append(token)

        for token in tokens:
            lemma = token[2].lower()

            if token[1] != "NOUN" or lemma not in noun_list:
                continue

            # 목록 명사를 핵어로 갖는 의존소 확인
            for dependent in dependents.get(token[3], []):
                if (
                    dependent[6] == "nmod:poss"
                    and dependent[0].lower() in possessives
                ):
                    noun_list[lemma].append(
                        (sentence_id, dependent[0], sentence_text)
                    )

    return noun_list


def extract_s_possessive_examples(corpus_data, noun_list):
    for sentence_id, tokens in corpus_data:
        sentence_text = " ".join(token[0] for token in tokens)

        # 핵어 ID별로 의존소를 모음
        dependents = {}
        for token in tokens:
            dependents.setdefault(token[4], []).append(token)

        for token in tokens:
            lemma = token[2].lower()

            if token[1] != "NOUN" or lemma not in noun_list:
                continue

            # 목록 명사의 의존소 X 확인
            for x in dependents.get(token[3], []):
                if x[6] != "nmod:poss":
                    continue

                # X의 의존소 하나가 두 조건을 모두 만족하는지 확인
                has_s_marker = any(
                    dependent[2].lower() == "'s"
                    and dependent[6] == "case"
                    for dependent in dependents.get(x[3], [])
                )

                if has_s_marker:
                    noun_list[lemma].append(
                        (sentence_id, x[0], sentence_text)
                    )

    return noun_list


def extract_of_examples(corpus_data, noun_list):
    excluded_lemmas = {"kind", "sort", "type"}

    for sentence_id, tokens in corpus_data:
        sentence_text = " ".join(token[0] for token in tokens)

        # 핵어 ID별로 의존소를 모음
        dependents = {}
        for token in tokens:
            dependents.setdefault(token[4], []).append(token)

        for token in tokens:
            lemma = token[2].lower()

            if token[1] != "NOUN" or lemma not in noun_list:
                continue

            # 목록 명사의 의존소 X 확인
            for x in dependents.get(token[3], []):
                if x[6] != "nmod":
                    continue

                if x[1] == "SYM":
                    continue

                if x[2].lower() in excluded_lemmas:
                    continue

                # X의 의존소 하나가 of와 case 조건을 모두 만족하는지 확인
                has_of_marker = any(
                    dependent[2].lower() == "of"
                    and dependent[6] == "case"
                    for dependent in dependents.get(x[3], [])
                )

                if has_of_marker:
                    noun_list[lemma].append(
                        (sentence_id, x[0], sentence_text)
                    )

    return noun_list


def extract_whose_examples(corpus_data, noun_list):
    for sentence_id, tokens in corpus_data:
        sentence_text = " ".join(token[0] for token in tokens)

        # 핵어 ID별로 의존소를 모음
        dependents = {}
        for token in tokens:
            dependents.setdefault(token[4], []).append(token)

        for token in tokens:
            lemma = token[2].lower()

            if token[1] != "NOUN" or lemma not in noun_list:
                continue

            # 같은 의존소에 대해 두 조건을 모두 확인
            for dependent in dependents.get(token[3], []):
                if (
                    dependent[6] == "nmod:poss"
                    and dependent[0].lower() == "whose"
                ):
                    noun_list[lemma].append(
                        (sentence_id, dependent[0], sentence_text)
                    )

    return noun_list
